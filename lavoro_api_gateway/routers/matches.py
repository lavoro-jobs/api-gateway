import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_applicant_user, get_current_recruiter_user
from lavoro_api_gateway.services import matches_service
from lavoro_library.model.auth_api.db_models import Account

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/get-matches-by-applicant")
def get_matches_by_applicant(current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return matches_service.get_matches_by_applicant(current_user.id)


@router.get("/get-matches-by-job-post/{job_post_id}")
def get_matches_by_job_post(
    job_post_id: uuid.UUID, current_user: Annotated[Account, Depends(get_current_recruiter_user)]
):
    return matches_service.get_matches_by_job_post(job_post_id)


@router.post("/reject-match/{job_post_id}")
def reject_match(job_post_id: uuid.UUID, current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return matches_service.reject_match(job_post_id, current_user.id)
