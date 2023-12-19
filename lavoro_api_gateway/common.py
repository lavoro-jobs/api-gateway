import uuid
from typing import List

import requests
from pydantic import EmailStr

from fastapi import HTTPException

from lavoro_api_gateway.amqp import producer
from lavoro_api_gateway.database.queries import (
    get_position_catalog,
    get_skills_catalog,
    get_education_catalog,
    get_contract_type_catalog,
    get_work_type_catalog,
)
from lavoro_library.model.api_gateway.dtos import ContractTypeDTO, EducationLevelDTO, PositionDTO, SkillDTO, WorkTypeDTO
from lavoro_library.model.applicant_api.db_models import ApplicantProfile, Experience
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.company_api.db_models import JobPost, RecruiterProfile
from lavoro_library.model.company_api.dtos import JobPostDTO
from lavoro_library.model.message_schemas import ApplicantProfileToMatch, ItemToMatch, JobPostToMatch


def propagate_response(response, response_model=None):
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"],
        )
    if response_model is None:
        return response.json()
    return response_model(**response.json())


def get_account(email: EmailStr):
    response = requests.get(f"http://auth-api/account/{email}")
    return propagate_response(response, response_model=Account)


def get_recruiter_profile(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile/{account_id}")
    return propagate_response(response, response_model=RecruiterProfile)


def get_recruiter_job_posts(account_id: uuid.UUID):
    job_posts_response = requests.get(f"http://company-api/job-post/get-job-posts-by-recruiter/{account_id}")
    job_posts = propagate_response(job_posts_response)
    job_posts = [JobPost(**job_post) for job_post in job_posts]

    hydrated_job_posts = []
    for job_post in job_posts:
        assignees_response = requests.get(f"http://company-api/job-post/get-assignees/{job_post.id}")
        assignees = propagate_response(assignees_response)
        assignees = [RecruiterProfile(**assignee) for assignee in assignees]

        hydrated_job_post: JobPostDTO = fill_database_model_with_catalog_data(
            JobPost(**job_post.model_dump()), JobPostDTO
        )
        hydrated_job_post.assignees = assignees
        hydrated_job_posts.append(hydrated_job_post)

    return hydrated_job_posts


def get_job_posts_by_company(company_id: uuid.UUID):
    job_posts_response = requests.get(f"http://company-api/job-post/get-job-posts-by-company/{company_id}")
    job_posts = propagate_response(job_posts_response)
    job_posts = [JobPost(**job_post) for job_post in job_posts]

    hydrated_job_posts = []
    for job_post in job_posts:
        assignees_response = requests.get(f"http://company-api/job-post/get-assignees/{job_post.id}")
        assignees = propagate_response(assignees_response)
        assignees = [RecruiterProfile(**assignee) for assignee in assignees]

        hydrated_job_post: JobPostDTO = fill_database_model_with_catalog_data(
            JobPost(**job_post.model_dump()), JobPostDTO
        )
        hydrated_job_post.assignees = assignees
        hydrated_job_posts.append(hydrated_job_post)

    return hydrated_job_posts


def fill_database_model_with_catalog_data(input_model, output_model_type):
    position_catalog = get_position_catalog()
    skills_catalog = get_skills_catalog()
    education_catalog = get_education_catalog()
    work_type_catalog = get_work_type_catalog()
    contract_type_catalog = get_contract_type_catalog()

    catalog_list = [
        {
            "name_in_db_model": "position_id",
            "name_in_dto": "position",
            "catalog": position_catalog,
            "dto_model": PositionDTO,
            "is_list": False,
        },
        {
            "name_in_db_model": "skill_ids",
            "name_in_dto": "skills",
            "catalog": skills_catalog,
            "dto_model": SkillDTO,
            "is_list": True,
        },
        {
            "name_in_db_model": "education_level_id",
            "name_in_dto": "education_level",
            "catalog": education_catalog,
            "dto_model": EducationLevelDTO,
            "is_list": False,
        },
        {
            "name_in_db_model": "work_type_id",
            "name_in_dto": "work_type",
            "catalog": work_type_catalog,
            "dto_model": WorkTypeDTO,
            "is_list": False,
        },
        {
            "name_in_db_model": "contract_type_id",
            "name_in_dto": "contract_type",
            "catalog": contract_type_catalog,
            "dto_model": ContractTypeDTO,
            "is_list": False,
        },
    ]

    output_dict = input_model.dict()

    for catalog in catalog_list:
        id_field_in_db_model = catalog["name_in_db_model"]
        dto_field_in_output_model = catalog["name_in_dto"]
        catalog_data = catalog["catalog"]
        dto_model = catalog["dto_model"]

        if id_field_in_db_model in input_model.dict():
            if catalog["is_list"] == False:
                id_value = getattr(input_model, id_field_in_db_model)
                corresponding_dto = next((dto for dto in catalog_data if dto.id == id_value), None)
            else:
                id_value_list = getattr(input_model, id_field_in_db_model)
                corresponding_dto = [dto for dto in catalog_data if dto.id in id_value_list]

            if corresponding_dto is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid {id_field_in_db_model} value: {id_value}",
                )

            if catalog["is_list"] == False:
                field = dto_model(**corresponding_dto.dict())
            else:
                field = [dto_model(**dto.dict()) for dto in corresponding_dto]

            output_dict[dto_field_in_output_model] = field

    output_model = output_model_type(**output_dict)

    return output_model


def generate_applicant_profile_to_match(applicant_profile: ApplicantProfile, experiences: List[Experience]):
    experience_years = 0 if len(experiences) == 0 else sum([experience.years for experience in experiences])
    applicant_profile_to_match = ApplicantProfileToMatch(
        applicant_account_id=applicant_profile.account_id,
        education_level_id=applicant_profile.education_level_id,
        skill_ids=applicant_profile.skill_ids,
        work_type_id=applicant_profile.work_type_id,
        seniority_level=applicant_profile.seniority_level,
        position_id=applicant_profile.position_id,
        home_location=applicant_profile.home_location,
        work_location_max_distance=applicant_profile.work_location_max_distance,
        contract_type_id=applicant_profile.contract_type_id,
        min_salary=applicant_profile.min_salary,
        experience_years=experience_years,
    )
    return ItemToMatch(data=applicant_profile_to_match)


def generate_job_post_to_match(job_post: JobPost):
    job_post_to_match = JobPostToMatch(
        job_post_id=job_post.id,
        position_id=job_post.position_id,
        education_level_id=job_post.education_level_id,
        skill_ids=job_post.skill_ids,
        work_type_id=job_post.work_type_id,
        work_location=job_post.work_location,
        contract_type_id=job_post.contract_type_id,
        salary_min=job_post.salary_min,
        salary_max=job_post.salary_max,
        seniority_level=job_post.seniority_level,
        end_date=job_post.end_date,
    )
    return ItemToMatch(data=job_post_to_match)


def publish_item_to_match(item_to_match: ItemToMatch):
    producer.publish(item_to_match)
