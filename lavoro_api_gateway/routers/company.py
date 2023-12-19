import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_company_admin_user, get_current_recruiter_user
from lavoro_api_gateway.dependencies.company_dependencies import (
    get_recruiter_job_posts,
    get_recruiter_profile,
    get_admin_recruiter_profile,
)


from lavoro_api_gateway.services import company_service


from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.api_gateway.dtos import JoinCompanyDTO
from lavoro_library.model.company_api.db_models import JobPost, RecruiterProfile, RecruiterRole
from lavoro_library.model.company_api.dtos import (
    CreateAssigneesDTO,
    CreateJobPostWithAssigneesDTO,
    CreateRecruiterProfileDTO,
    CreateCompanyDTO,
    UpdateCompanyDTO,
    UpdateJobPostDTO,
    UpdateRecruiterProfileDTO,
)


router = APIRouter(prefix="/company", tags=["company"])


@router.post("/create-recruiter-profile")
def create_recruiter_profile(
    current_user: Annotated[Account, Depends(get_current_company_admin_user)], payload: CreateRecruiterProfileDTO
):
    return company_service.create_recruiter_profile(current_user.id, RecruiterRole.admin, payload)


@router.patch("/update-recruiter-profile", status_code=status.HTTP_200_OK)
def update_recruiter_profile(
    current_user: Annotated[Account, Depends(get_current_recruiter_user)],
    payload: UpdateRecruiterProfileDTO,
):
    return company_service.update_recruiter_profile(current_user.id, payload)


@router.post("/create-company")
def create_company(
    current_user: Annotated[Account, Depends(get_current_company_admin_user)], payload: CreateCompanyDTO
):
    return company_service.create_company(current_user.id, payload)


@router.get("/get-company")
def get_company(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)],
):
    return company_service.get_company(recruiter_profile.company_id)


@router.get("/get-company-with-recruiters")
def get_company_with_recruiters(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)],
):
    return company_service.get_company_with_recruiters(recruiter_profile.company_id)


@router.patch("/update-company")
def update_company(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_admin_recruiter_profile)],
    payload: UpdateCompanyDTO,
):
    return company_service.update_company(recruiter_profile.company_id, payload)


@router.get("/get-recruiter-profile")
def get_recruiter(current_user: Annotated[Account, Depends(get_current_recruiter_user)]):
    return company_service.get_recruiter_profile_with_company_name(current_user.id)


@router.post("/invite-recruiter/{new_recruiter_email}")
def invite_recruiter(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_admin_recruiter_profile)], new_recruiter_email: EmailStr
):
    return company_service.invite_recruiter(recruiter_profile.company_id, new_recruiter_email)


@router.post("/join-company/{invite_token}")
def join_company(invite_token: str, payload: JoinCompanyDTO):
    return company_service.join_company(invite_token, payload)


@router.post("/create-job-post")
def create_job_post(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)],
    payload: CreateJobPostWithAssigneesDTO,
):
    return company_service.create_job_post(recruiter_profile.company_id, recruiter_profile.account_id, payload)


@router.patch("/update-job-post/{job_post_id}", status_code=status.HTTP_200_OK)
def update_job_post(
    job_post_id: uuid.UUID,
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
    payload: UpdateJobPostDTO,
):
    job_post_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_post_ids:
        raise HTTPException(status_code=400, detail="Recruiter is not assigned to this job post")
    return company_service.update_job_post(job_post_id, payload)


@router.patch("/soft-delete-job-post/{job_post_id}", status_code=status.HTTP_200_OK)
def soft_delete_job_post(job_post_id: uuid.UUID, job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)]):
    job_post_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_post_ids:
        raise HTTPException(status_code=400, detail="Recruiter is not assigned to this job post")
    return company_service.soft_delete_job_post(job_post_id)


@router.post("/assign-job-post/{job_post_id}")
def assign_job_post(
    job_post_id: uuid.UUID,
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
    payload: CreateAssigneesDTO,
):
    job_post_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_post_ids:
        raise HTTPException(status_code=400, detail="Recruiter is not assigned to this job post")
    return company_service.assign_job_post(job_post_id, payload)


@router.get("/get-job-posts-by-company")
def get_job_posts_by_company(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_admin_recruiter_profile)],
):
    return company_service.get_job_posts_by_company(recruiter_profile.company_id)


@router.get("/get-job-posts-by-recruiter")
def get_job_posts_by_recruiter(
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
):
    return job_posts
