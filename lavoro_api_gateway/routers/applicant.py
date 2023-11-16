import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_applicant_user
from lavoro_api_gateway.helpers.applicant_helpers import create_applicant_profile
from lavoro_library.models import CreateApplicantProfileRequest, UserInDB


router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.post("/create_applicant_profile", status_code=status.HTTP_201_CREATED)
def create_applicant(
    current_user: Annotated[UserInDB, Depends(get_current_applicant_user)],
    payload: Annotated[CreateApplicantProfileRequest, Depends()],
):
    applicant_id = create_applicant_profile(current_user.id, payload)
    return {"applicant_id": applicant_id}
