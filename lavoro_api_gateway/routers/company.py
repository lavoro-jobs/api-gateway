from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
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
)


router = APIRouter(prefix="/company", tags=["company"])


@router.post("/create-recruiter-profile")
def create_recruiter_profile(
    current_user: Annotated[Account, Depends(get_current_company_admin_user)], payload: CreateRecruiterProfileDTO
):
    return company_service.create_recruiter_profile(current_user.id, RecruiterRole.admin, payload)


@router.post("/create-company")
def create_company(
    current_user: Annotated[Account, Depends(get_current_company_admin_user)], payload: CreateCompanyDTO
):
    return company_service.create_company(current_user.id, payload)


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
