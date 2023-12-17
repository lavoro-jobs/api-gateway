from typing import List
import uuid
from fastapi import HTTPException
from pydantic import EmailStr
import requests

from fastapi.encoders import jsonable_encoder

from lavoro_api_gateway.common import (
    fill_database_model_with_catalog_data,
    generate_job_post_to_match,
    get_account,
    propagate_response,
    publish_item_to_match,
)
from lavoro_library.model.api_gateway.dtos import JoinCompanyDTO
from lavoro_library.model.auth_api.db_models import Role
from lavoro_library.model.auth_api.dtos import RegisterDTO
from lavoro_library.model.company_api.db_models import Assignee, JobPost, RecruiterProfile, RecruiterRole
from lavoro_library.model.company_api.dtos import (
    CompanyDTO,
    CompanyWithRecruitersDTO,
    CreateAssigneesDTO,
    CreateJobPostWithAssigneesDTO,
    CreateRecruiterProfileDTO,
    InviteTokenDTO,
    JobPostDTO,
    RecruiterProfileDTO,
    RecruiterProfileWithCompanyNameDTO,
    UpdateJobPostDTO,
    UpdateRecruiterProfileDTO,
)


def create_recruiter_profile(account_id: uuid.UUID, recruiter_role: RecruiterRole, payload: CreateRecruiterProfileDTO):
    response = requests.post(
        f"http://company-api/recruiter/create-recruiter-profile/{account_id}/{recruiter_role}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def update_recruiter_profile(account_id: uuid.UUID, payload: UpdateRecruiterProfileDTO):
    response = requests.patch(
        f"http://company-api/recruiter/update-recruiter-profile/{account_id}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def get_recruiter_profile(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile/{account_id}")
    return propagate_response(response, response_model=RecruiterProfileDTO)


def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile-with-company-name/{account_id}")
    return propagate_response(response, response_model=RecruiterProfileWithCompanyNameDTO)


def create_company(account_id: uuid.UUID, payload):
    response = requests.post(
        f"http://company-api/company/create-company/{account_id}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def get_company(company_id: uuid.UUID):
    response = requests.get(f"http://company-api/company/get-company/{company_id}")
    return propagate_response(response, CompanyDTO)


def get_company_with_recruiters(company_id: uuid.UUID):
    company_response = requests.get(f"http://company-api/company/get-company/{company_id}")
    company = propagate_response(company_response, response_model=CompanyWithRecruitersDTO)

    recruiters_response = requests.get(f"http://company-api/recruiter/get-recruiters-by-company/{company_id}")
    recruiters = propagate_response(recruiters_response)

    company.recruiters = recruiters
    return company


def invite_recruiter(company_id: uuid.UUID, new_recruiter_email: EmailStr):
    user = None
    try:
        user = get_account(new_recruiter_email)
    except HTTPException as e:
        pass

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    response = requests.post(
        f"http://company-api/company/invite-recruiter/{company_id}/{new_recruiter_email}",
    )
    return propagate_response(response)


def join_company(invite_token: str, payload: JoinCompanyDTO):
    invitation_response = requests.get(f"http://company-api/recruiter/get-invitation/{invite_token}")
    invitation = propagate_response(invitation_response, response_model=InviteTokenDTO)
    register_request = RegisterDTO(email=invitation.email, password=payload.password, role=Role.recruiter)
    register_response = requests.post(
        f"http://auth-api/register/no-confirm",
        data=jsonable_encoder(register_request),
    )
    propagate_response(register_response)
    user = get_account(invitation.email)
    create_recruiter_profile_request = CreateRecruiterProfileDTO(
        company_id=invitation.company_id, first_name=payload.first_name, last_name=payload.last_name
    )
    create_recruiter_profile_response = requests.post(
        f"http://company-api/recruiter/create-recruiter-profile/{user.id}/{RecruiterRole.employee}",
        json=jsonable_encoder(create_recruiter_profile_request),
        headers={"Content-Type": "application/json"},
    )
    delete_invite_token_response = requests.delete(f"http://company-api/company/delete-invite-token/{invite_token}")
    propagate_response(create_recruiter_profile_response)
    propagate_response(delete_invite_token_response)
    return


def create_job_post(company_id: uuid.UUID, recruiter_account_id: uuid.UUID, payload: CreateJobPostWithAssigneesDTO):
    job_post_request = payload.model_dump(exclude={"assignees"})
    job_post_response = requests.post(
        f"http://company-api/job-post/create-job-post/{company_id}",
        json=jsonable_encoder(job_post_request),
        headers={"Content-Type": "application/json"},
    )
    job_post = propagate_response(job_post_response, response_model=JobPost)
    print(job_post)

    assignees_request = payload.assignees
    assignees_request.append(recruiter_account_id)
    assignees_response = requests.post(
        f"http://company-api/job-post/create-assignees/{job_post.id}",
        json=jsonable_encoder(assignees_request),
        headers={"Content-Type": "application/json"},
    )
    assignees = propagate_response(assignees_response)
    assignees = [Assignee(**assignee) for assignee in assignees]

    message = generate_job_post_to_match(job_post)
    publish_item_to_match(message)


def update_job_post(job_post_id: uuid.UUID, payload: UpdateJobPostDTO):
    response = requests.patch(
        f"http://company-api/job-post/update-job-post/{job_post_id}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    job_post = propagate_response(response, response_model=JobPost)
    message = generate_job_post_to_match(job_post)
    publish_item_to_match(message)


def soft_delete_job_post(job_post_id: uuid.UUID):
    response = requests.patch(f"http://company-api/job-post/soft-delete-job-post/{job_post_id}")
    job_post = propagate_response(response, response_model=JobPost)
    message = generate_job_post_to_match(job_post)
    publish_item_to_match(message)


def assign_job_post(job_post_id: uuid.UUID, payload: CreateAssigneesDTO):
    response = requests.post(
        f"http://company-api/job-post/create-assignees/{job_post_id}",
        json=jsonable_encoder(payload.assignees),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def get_job_posts_by_company(company_id: uuid.UUID):
    job_posts_response = requests.get(f"http://company-api/job-post/get-job-posts-by-company/{company_id}")
    job_posts = propagate_response(job_posts_response)
    job_posts = [JobPost(**job_post) for job_post in job_posts]

    hydrated_job_posts = []
    for job_post in job_posts:
        assignees_response = requests.get(f"http://company-api/job-post/get-assignees/{job_post.id}")
        assignees = propagate_response(assignees_response)
        assignees = [RecruiterProfile(**assignee) for assignee in assignees]

        hydrated_job_post: JobPostDTO = fill_database_model_with_catalog_data(
            JobPost(**job_post.model_dump()), JobPostDTO
        )
        hydrated_job_post.assignees = assignees
        hydrated_job_posts.append(hydrated_job_post)

    return hydrated_job_posts


def get_job_posts_by_recruiter(recruiter_account_id: uuid.UUID):
    job_posts_response = requests.get(f"http://company-api/job-post/get-job-posts-by-recruiter/{recruiter_account_id}")
    job_posts = propagate_response(job_posts_response)
    job_posts = [JobPost(**job_post) for job_post in job_posts]

    hydrated_job_posts = []
    for job_post in job_posts:
        assignees_response = requests.get(f"http://company-api/job-post/get-assignees/{job_post.id}")
        assignees = propagate_response(assignees_response)
        assignees = [RecruiterProfile(**assignee) for assignee in assignees]

        hydrated_job_post: JobPostDTO = fill_database_model_with_catalog_data(
            JobPost(**job_post.model_dump()), JobPostDTO
        )
        hydrated_job_post.assignees = assignees
        hydrated_job_posts.append(hydrated_job_post)

    return hydrated_job_posts
