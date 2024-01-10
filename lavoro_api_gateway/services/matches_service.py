from typing import List
import uuid
from fastapi.encoders import jsonable_encoder
import requests

from lavoro_api_gateway.common import fill_database_model_with_catalog_data, propagate_response
from lavoro_library.model.applicant_api.db_models import ApplicantProfile, Experience
from lavoro_library.model.applicant_api.dtos import ApplicantProfileDTO, ApplicantProfileForJobPostDTO, ExperienceDTO
from lavoro_library.model.company_api.db_models import JobPost
from lavoro_library.model.company_api.dtos import CompanyDTO, JobPostDTO, JobPostForApplicantDTO, RecruiterProfileDTO
from lavoro_library.model.matching_api.db_models import Match
from lavoro_library.model.matching_api.dtos import (
    ApplicantMatchDTO,
    ApplicationDTO,
    CommentDTO,
    CreateCommentDTO,
    JobPostMatchDTO,
)


def get_matches_by_applicant(applicant_account_id: uuid.UUID):
    matches_response = requests.get(f"http://matching-api/matches/get-matches-by-applicant/{applicant_account_id}")
    matches = propagate_response(matches_response)
    matches = [Match(**match) for match in matches]

    for match in matches:
        job_post_response = requests.get(f"http://company-api/job-post/get-job-post/{match.job_post_id}")
        job_post = propagate_response(job_post_response, response_model=JobPost)

        company_response = requests.get(f"http://company-api/company/get-company/{job_post.company_id}")
        company = propagate_response(company_response, response_model=CompanyDTO)

        job_post: JobPostDTO = fill_database_model_with_catalog_data(job_post, JobPostDTO)
        job_post_for_applicant = JobPostForApplicantDTO(
            **job_post.model_dump(),
            company=company,
        )

        applicant_match = ApplicantMatchDTO(
            job_post=job_post_for_applicant,
            match_score=match.match_score,
            approved_by_applicant=match.approved_by_applicant,
            created_on_date=match.created_on_date,
            end_date=match.end_date,
        )
        yield applicant_match


def get_matches_by_job_post(job_post_id: uuid.UUID):
    matches_response = requests.get(f"http://matching-api/matches/get-matches-by-job-post/{job_post_id}")
    matches = propagate_response(matches_response)
    matches = [Match(**match) for match in matches]

    for match in matches:
        applicant_profile_response = requests.get(
            f"http://applicant-api/applicant/get-applicant-profile/{match.applicant_account_id}"
        )
        applicant_profile = propagate_response(applicant_profile_response, response_model=ApplicantProfile)
        applicant_profile = fill_database_model_with_catalog_data(applicant_profile, ApplicantProfileDTO)
        applicant_profile_for_job_post = ApplicantProfileForJobPostDTO(**applicant_profile.model_dump())

        applicant_match = JobPostMatchDTO(
            applicant_profile=applicant_profile_for_job_post,
            match_score=match.match_score,
            approved_by_applicant=match.approved_by_applicant,
            created_on_date=match.created_on_date,
            end_date=match.end_date,
        )
        yield applicant_match


def reject_match(job_post_id: uuid.UUID, applicant_account_id: uuid.UUID):
    response = requests.post(f"http://matching-api/matches/reject-match/{job_post_id}/{applicant_account_id}")
    return propagate_response(response)


def get_applications_by_job_post(job_post_id: uuid.UUID):
    response = requests.get(f"http://matching-api/application/get-applications-by-job-post/{job_post_id}")
    applications = propagate_response(response)
    applications_dtos = [ApplicationDTO(**application) for application in applications]

    for application in applications_dtos:
        comments_response = requests.get(
            f"http://matching-api/application/get-comments-on-application/{job_post_id}/{application.applicant_account_id}"
        )
        comments = propagate_response(comments_response)
        comments = [CommentDTO(**comment) for comment in comments]
        for comment in comments:
            recruiter_profile_response = requests.get(
                f"http://company-api/recruiter/get-recruiter-profile/{comment.account_id}"
            )
            recruiter_profile = propagate_response(recruiter_profile_response, response_model=RecruiterProfileDTO)
            comment.recruiter = recruiter_profile

        application.comments = comments

        applicant_profile_response = requests.get(
            f"http://applicant-api/applicant/get-applicant-profile/{application.applicant_account_id}"
        )
        applicant_profile = propagate_response(applicant_profile_response, response_model=ApplicantProfile)

        experiences_response = requests.get(
            f"http://applicant-api/applicant/get-experiences/{application.applicant_account_id}"
        )
        experiences = propagate_response(experiences_response)

        hydrated_applicant_profile: ApplicantProfileDTO = fill_database_model_with_catalog_data(
            applicant_profile, ApplicantProfileDTO
        )
        hydrated_experiences: List[ExperienceDTO] = []
        for experience in experiences:
            hydrated_experience = fill_database_model_with_catalog_data(Experience(**experience), ExperienceDTO)
            hydrated_experiences.append(hydrated_experience)

        hydrated_applicant_profile.experiences = hydrated_experiences
        application.applicant = hydrated_applicant_profile

        applicant_stream_chat_token_response = requests.get(
            f"http://auth-api/account/get-stream-chat-token/{application.applicant_account_id}"
        )
        applicant_stream_chat_token = propagate_response(applicant_stream_chat_token_response)["stream_chat_token"]
        application.applicant_stream_chat_token = applicant_stream_chat_token

        assignees_response = requests.get(f"http://company-api/job-post/get-assignees/{job_post_id}")
        assignees = propagate_response(assignees_response)
        assignees_dto = [RecruiterProfileDTO(**assignee) for assignee in assignees]

        assignees_stream_chat_tokens = []
        for assignee in assignees_dto:
            assignee_stream_chat_token_response = requests.get(
                f"http://auth-api/account/get-stream-chat-token/{assignee.account_id}"
            )
            assignee_stream_chat_token = propagate_response(assignee_stream_chat_token_response)["stream_chat_token"]
            assignees_stream_chat_tokens.append(assignee_stream_chat_token)

        application.assignees_stream_chat_tokens = assignees_stream_chat_tokens

    return applications_dtos


def get_created_applications_by_applicant(applicant_account_id: uuid.UUID):
    response = requests.get(
        f"http://matching-api/application/get-created-applications-by-applicant/{applicant_account_id}"
    )
    applications = propagate_response(response)
    applications_dtos = [ApplicationDTO(**application) for application in applications]
    return applications_dtos


def approve_application(job_post_id: uuid.UUID, applicant_account_id: uuid.UUID):
    response = requests.patch(
        f"http://matching-api/application/approve-application/{job_post_id}/{applicant_account_id}"
    )
    return propagate_response(response)


def reject_application(job_post_id: uuid.UUID, applicant_account_id: uuid.UUID):
    response = requests.patch(
        f"http://matching-api/application/reject-application/{job_post_id}/{applicant_account_id}"
    )
    return propagate_response(response)


def create_application(job_post_id: uuid.UUID, applicant_account_id: uuid.UUID):
    response = requests.post(f"http://matching-api/application/create-application/{job_post_id}/{applicant_account_id}")
    return propagate_response(response)


def comment_application(
    job_post_id: uuid.UUID, applicant_account_id: uuid.UUID, current_recruiter_id: uuid.UUID, payload: CreateCommentDTO
):
    response = requests.post(
        f"http://matching-api/application/comment-application/{current_recruiter_id}/{job_post_id}/{applicant_account_id}",
        json=jsonable_encoder(payload),
    )
    return propagate_response(response)


def get_comments_on_application(job_post_id: uuid.UUID, applicant_account_id: uuid.UUID):
    response = requests.get(
        f"http://matching-api/application/get-comments-on-application/{job_post_id}/{applicant_account_id}"
    )
    comments = propagate_response(response)
    comments = [CommentDTO(**comment) for comment in comments]

    for comment in comments:
        recruiter_profile_response = requests.get(
            f"http://company-api/recruiter/get-recruiter-profile/{comment.account_id}"
        )
        recruiter_profile = propagate_response(recruiter_profile_response, response_model=RecruiterProfileDTO)
        comment.recruiter = recruiter_profile

    return comments


def delete_comment(job_post_id: uuid.UUID, comment_id: uuid.UUID):
    response = requests.delete(f"http://matching-api/application/delete-comment/{job_post_id}/{comment_id}")
    return propagate_response(response)
