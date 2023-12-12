import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_applicant_user

from lavoro_api_gateway.services import applicant_service

from lavoro_library.model.applicant_api.dtos import (
    CreateExperienceDTO,
    CreateApplicantProfileWithExperiencesDTO,
    UpdateApplicantExperienceDTO,
    UpdateApplicantProfileDTO,
)
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


@router.patch("/update-applicant-profile", status_code=status.HTTP_200_OK)
def update_applicant_profile(
    current_user: Annotated[Account, Depends(get_current_applicant_user)],
    payload: UpdateApplicantProfileDTO,
):
    return applicant_service.update_applicant_profile(current_user.id, payload)


@router.patch("/update-applicant-experience/{experience_id}", status_code=status.HTTP_200_OK)
def update_applicant_experience(
    experience_id: uuid.UUID,
    payload: UpdateApplicantExperienceDTO,
    current_user: Annotated[Account, Depends(get_current_applicant_user)],
):
    return applicant_service.update_applicant_experience(experience_id, payload)


@router.delete("/delete-applicant-experience/{experience_id}", status_code=status.HTTP_200_OK)
def delete_applicant_experience(
    experience_id: uuid.UUID,
    current_user: Annotated[Account, Depends(get_current_applicant_user)],
):
    return applicant_service.delete_applicant_experience(experience_id)
