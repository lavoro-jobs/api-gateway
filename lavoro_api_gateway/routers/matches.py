import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_applicant_user, get_current_recruiter_user
from lavoro_api_gateway.dependencies.company_dependencies import get_recruiter_job_posts
from lavoro_api_gateway.services import matches_service
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.company_api.db_models import JobPost
from lavoro_library.model.matching_api.dtos import CreateCommentDTO

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


@router.get("/get-applications-by-job-post/{job_post_id}")
def get_applications_by_job_post(
    job_post_id: uuid.UUID, job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)]
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to this job post")
    return matches_service.get_applications_by_job_post(job_post_id)


@router.get("/get-created-applications-by-applicant")
def get_created_applications_by_applicant(current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return matches_service.get_created_applications_by_applicant(current_user.id)


@router.patch("/approve-application/{job_post_id}/{applicant_account_id}")
def approve_application(
    job_post_id: uuid.UUID,
    applicant_account_id: uuid.UUID,
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to this job post")
    return matches_service.approve_application(job_post_id, applicant_account_id)


@router.patch("/reject-application/{job_post_id}/{applicant_account_id}")
def reject_application(
    job_post_id: uuid.UUID,
    applicant_account_id: uuid.UUID,
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to this job post")
    return matches_service.reject_application(job_post_id, applicant_account_id)


@router.post("/create-application/{job_post_id}")
def create_application(job_post_id: uuid.UUID, current_user: Annotated[Account, Depends(get_current_applicant_user)]):
    return matches_service.create_application(job_post_id, current_user.id)


@router.post("/comment-application/{job_post_id}/{applicant_account_id}")
def comment_application(
    job_post_id: uuid.UUID,
    applicant_account_id: uuid.UUID,
    payload: CreateCommentDTO,
    current_recruiter: Annotated[Account, Depends(get_current_recruiter_user)],
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to the job post of this application")
    return matches_service.comment_application(job_post_id, applicant_account_id, current_recruiter.id, payload)


@router.get("/get-comments-on-application/{job_post_id}/{applicant_account_id}")
def get_comments_on_application(
    job_post_id: uuid.UUID,
    applicant_account_id: uuid.UUID,
    current_recruiter: Annotated[Account, Depends(get_current_recruiter_user)],
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to the job post of this application")
    return matches_service.get_comments_on_application(job_post_id, applicant_account_id)


@router.delete("/delete-comment/{job_post_id}/{comment_id}")
def delete_comment(
    job_post_id: uuid.UUID,
    comment_id: uuid.UUID,
    current_recruiter: Annotated[Account, Depends(get_current_recruiter_user)],
    job_posts: Annotated[List[JobPost], Depends(get_recruiter_job_posts)],
):
    job_posts_ids = [job_post.id for job_post in job_posts]
    if job_post_id not in job_posts_ids:
        raise HTTPException(status_code=404, detail="Recruiter is not assigned to the job post of this application")
    return matches_service.delete_comment(job_post_id, comment_id)
