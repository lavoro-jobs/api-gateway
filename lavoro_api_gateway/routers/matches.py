import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_applicant_user
from lavoro_api_gateway.dependencies.company_dependencies import get_recruiter_job_posts
from lavoro_api_gateway.services import matches_service
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.company_api.db_models import JobPost

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/get-matches-by-applicant")
def get_matches_by_applicant(current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return matches_service.get_matches_by_applicant(current_user.id)


@router.get("/get-matches-by-job-post/{job_post_id}")
def get_matches_by_job_post(
    job_post_id: uuid.UUID, job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)]
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to this job post")
    return matches_service.get_matches_by_job_post(job_post_id)


@router.post("/reject-match/{job_post_id}")
def reject_match(job_post_id: uuid.UUID, current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return matches_service.reject_match(job_post_id, current_user.id)


@router.get("/get-applications-to-job-post/{job_post_id}")
def get_applications_to_job_post(
    job_post_id: uuid.UUID, job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)]
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to this job post")
    return matches_service.get_applications_to_job_post(job_post_id)


@router.post("/approve-application/{job_post_id}/{applicant_account_id}")
def approve_application(
    job_post_id: uuid.UUID,
    applicant_account_id: uuid.UUID,
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to this job post")
    return matches_service.approve_application(job_post_id, applicant_account_id)


@router.post("/create-application/{job_post_id}")
def create_application(job_post_id: uuid.UUID, current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return matches_service.create_application(job_post_id, current_user.id)
