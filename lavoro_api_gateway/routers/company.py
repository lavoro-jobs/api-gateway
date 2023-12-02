from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_company_admin_user, get_current_recruiter_user
from lavoro_api_gateway.dependencies.company_dependencies import get_recruiter_profile
from lavoro_api_gateway.helpers.company_helpers import (
    check_invite_token,
    create_company_profile,
    create_recruiter_profile,
    delete_invite_token,
    get_recruiter_profile_with_company_name,
    invite_recruiter_to_company,
)
from lavoro_api_gateway.helpers.auth_helpers import register_user_no_confirm, get_account

from lavoro_library.models import (
    CreateCompanyRequest,
    CreateRecruiterProfileRequest,
    JoinCompanyRequest,
    RecruiterProfileInDB,
    RecruiterProfileWithCompanyName,
    RegistrationForm,
    Role,
    UserInDB,
    RecruiterRole,
)


router = APIRouter(prefix="/company", tags=["company"])


@router.post("/create-recruiter-profile")
def create_recruiter(
    current_user: Annotated[UserInDB, Depends(get_current_company_admin_user)], payload: CreateRecruiterProfileRequest
):
    recruiter_profile_request = CreateRecruiterProfileRequest(**payload.model_dump())
    return create_recruiter_profile(recruiter_profile_request, current_user.id, RecruiterRole.admin)


@router.post("/create-company")
def create_company(
    current_user: Annotated[UserInDB, Depends(get_current_company_admin_user)], payload: CreateCompanyRequest
):
    return create_company_profile(payload, current_user.id)


@router.get("/get-recruiter-profile")
def get_recruiter(current_user: Annotated[RecruiterProfileWithCompanyName, Depends(get_current_recruiter_user)]):
    return get_recruiter_profile_with_company_name(current_user.id)


@router.post("/invite-recruiter/{new_recruiter_email}")
def invite_recruiter(
    recruiter_profile: Annotated[RecruiterProfileInDB, Depends(get_recruiter_profile)], new_recruiter_email: str
):
    try:
        user = get_account(new_recruiter_email)
    except HTTPException as e:
        return invite_recruiter_to_company(new_recruiter_email, recruiter_profile.company_id)
    raise HTTPException(status_code=400, detail="User already exists")


@router.post("/join-company/{invite_token}")
def join_company(invite_token: str, payload: JoinCompanyRequest):
    invitation = check_invite_token(invite_token)
    form_data = RegistrationForm(email=invitation.email, password=payload.password, role=Role.recruiter)
    register_user_no_confirm(form_data)
    user = get_account(invitation.email)
    recruiter_profile_request = CreateRecruiterProfileRequest(
        first_name=payload.first_name, last_name=payload.last_name, company_id=invitation.company_id
    )
    create_recruiter_profile(recruiter_profile_request, user.id, RecruiterRole.employee)
    delete_invite_token(invite_token)
    return {"detail": "Recruiter added to company"}
