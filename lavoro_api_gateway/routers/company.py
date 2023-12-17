from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_company_admin_user, get_current_recruiter_user
from lavoro_api_gateway.dependencies.company_dependencies import get_recruiter_profile, get_admin_recruiter_profile


from lavoro_api_gateway.services import company_service


from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.api_gateway.dtos import JoinCompanyDTO
from lavoro_library.model.company_api.db_models import RecruiterProfile, RecruiterRole
from lavoro_library.model.company_api.dtos import (
    CreateAssigneesDTO,
    CreateJobPostWithAssigneesDTO,
    CreateRecruiterProfileDTO,
    CreateCompanyDTO,
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
def update_applicant_profile(
    job_post_id: uuid.UUID,
    payload: UpdateJobPostDTO,
):
    return company_service.update_job_post(job_post_id, payload)


@router.patch("/soft-delete-job-post/{job_post_id}", status_code=status.HTTP_200_OK)
def soft_delete_job_post(
    job_post_id: uuid.UUID,
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)],
):
    return company_service.soft_delete_job_post(job_post_id)


@router.post("/assign-job-post/{job_post_id}")
def assign_job_post(
    job_post_id: uuid.UUID,
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)],
    payload: CreateAssigneesDTO,
):
    return company_service.assign_job_post(job_post_id, payload)


@router.get("/get-job-posts-by-company")
def get_job_posts_by_company(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_admin_recruiter_profile)],
):
    return company_service.get_job_posts_by_company(recruiter_profile.company_id)


@router.get("/get-job-posts-by-recruiter")
def get_job_posts_by_recruiter(
    recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)],
):
    return company_service.get_job_posts_by_recruiter(recruiter_profile.account_id)
