import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_applicant_user

# from lavoro_api_gateway.helpers.applicant_helpers import create_applicant_profile, get_applicant_profile
from lavoro_api_gateway.services import applicant_service

# from lavoro_library.models import CreateApplicantProfileRequest, UserInDB
from lavoro_library.model.applicant_api.dtos import CreateExperienceDTO, CreateApplicantProfileWithExperiencesDTO
from lavoro_library.model.auth_api.db_models import Account

router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.post("/create-applicant-profile", status_code=status.HTTP_201_CREATED)
def create_applicant_profile(
    current_user: Annotated[Account, Depends(get_current_applicant_user)],
    payload: CreateApplicantProfileWithExperiencesDTO,
):
    return applicant_service.create_applicant_profile(current_user.id, payload)
    # return create_applicant_profile(current_user.id, payload)


@router.post("/create-experiences", status_code=status.HTTP_201_CREATED)
def create_experiences(
    current_user: Annotated[Account, Depends(get_current_applicant_user)],
    payload: List[CreateExperienceDTO],
):
    return applicant_service.create_experiences(current_user.id, payload)
    # return create_experiences(current_user.id, payload)


@router.get("/get-applicant-profile")
def get_applicant_profile(current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return applicant_service.get_applicant_profile(current_user.id)
    # return get_applicant_profile(current_user.id)
