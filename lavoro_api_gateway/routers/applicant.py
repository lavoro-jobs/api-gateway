import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_applicant_user
from lavoro_api_gateway.helpers.applicant_helpers import create_applicant_profile, get_applicant_profile

# from lavoro_library.models import CreateApplicantProfileRequest, UserInDB
from lavoro_library.model.applicant_api.dtos import CreateApplicantProfileDTO
from lavoro_library.model.auth_api.db_models import Account

router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.post("/create-applicant-profile", status_code=status.HTTP_201_CREATED)
def create_applicant(
    current_user: Annotated[Account, Depends(get_current_applicant_user)],
    payload: CreateApplicantProfileDTO,
):
    return create_applicant_profile(current_user.id, payload)


@router.get("/get-applicant-profile")
def get_applicant(current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return get_applicant_profile(current_user.id)
