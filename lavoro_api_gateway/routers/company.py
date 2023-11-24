from typing import Annotated

from fastapi import APIRouter, Depends

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_company_admin_user, get_current_recruiter_user
from lavoro_api_gateway.helpers.company_helpers import (
    create_company_profile,
    create_recruiter_profile,
    get_recruiter_profile_with_company_name,
)
from lavoro_library.models import (
    CreateCompanyRequest,
    CreateRecruiterProfileRequest,
    RecruiterProfileWithCompanyName,
    UserInDB,
)


router = APIRouter(prefix="/company", tags=["company"])


@router.post("/create-recruiter-profile")
def create_recruiter(
    current_user: Annotated[UserInDB, Depends(get_current_company_admin_user)], payload: CreateRecruiterProfileRequest
):
    return create_recruiter_profile(payload, current_user.id)


@router.post("/create-company")
def create_company(
    current_user: Annotated[UserInDB, Depends(get_current_company_admin_user)], payload: CreateCompanyRequest
):
    return create_company_profile(payload, current_user.id)


@router.get("/get-recruiter-profile")
def get_recruiter(current_user: Annotated[RecruiterProfileWithCompanyName, Depends(get_current_recruiter_user)]):
    return get_recruiter_profile_with_company_name(current_user.id)
