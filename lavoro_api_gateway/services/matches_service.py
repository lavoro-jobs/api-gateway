import uuid
from fastapi.encoders import jsonable_encoder
import requests

from lavoro_api_gateway.common import fill_database_model_with_catalog_data, propagate_response
from lavoro_library.model.applicant_api.db_models import ApplicantProfile
from lavoro_library.model.applicant_api.dtos import ApplicantProfileDTO, ApplicantProfileForJobPostDTO
from lavoro_library.model.company_api.db_models import JobPost
from lavoro_library.model.company_api.dtos import CompanyDTO, JobPostDTO, JobPostForApplicantDTO
from lavoro_library.model.matching_api.db_models import Match
from lavoro_library.model.matching_api.dtos import ApplicantMatchDTO, ApplicationDTO, CreateCommentDTO, JobPostMatchDTO


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


def get_applications_to_job_post(job_post_id: uuid.UUID):
    response = requests.get(f"http://matching-api/application/get-applications-to-job-post/{job_post_id}")
    applications = propagate_response(response)
    applications_dtos = [ApplicationDTO(**application) for application in applications]
    return applications_dtos


def get_created_applications_by_applicant(applicant_account_id: uuid.UUID):
    response = requests.get(
        f"http://matching-api/application/get-created-applications-by-applicant/{applicant_account_id}"
    )
    applications = propagate_response(response)
    applications_dtos = [ApplicationDTO(**application) for application in applications]
    return applications_dtos


def approve_application(job_post_id: uuid.UUID, applicant_account_id: uuid.UUID):
    response = requests.post(
        f"http://matching-api/application/approve-application/{job_post_id}/{applicant_account_id}"
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
