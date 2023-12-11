import uuid
import requests

from fastapi.encoders import jsonable_encoder

from lavoro_api_gateway.database.queries import (
    get_education_catalog,
    get_position_catalog,
    get_skills_catalog,
    get_work_type_catalog,
    get_contract_type_catalog,
)
from lavoro_api_gateway.helpers.request_helpers import propagate_response

from lavoro_library.model.applicant_api.dtos import ApplicantProfileDTO, CreateApplicantProfileDTO, ExperienceDTO
from lavoro_library.model.applicant_api.db_models import ApplicantProfile


def create_applicant_profile(account_id: uuid.UUID, payload: CreateApplicantProfileDTO):
    response = requests.post(
        f"http://applicant-api/applicant/create-applicant-profile/{account_id}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def get_applicant_profile(account_id: uuid.UUID):
    applicant_profile_response = requests.get(f"http://applicant-api/applicant/get-applicant-profile/{account_id}")
    if applicant_profile_response.status_code >= 400:
        propagate_response(applicant_profile_response)

    experiences_response = requests.get(f"http://applicant-api/applicant/get-experiences/{account_id}")
    if experiences_response.status_code == 404:
        experiences = []
    elif experiences_response.status_code >= 400:
        propagate_response(experiences_response)
    else:
        experiences = [ExperienceDTO(**experience) for experience in experiences_response.json()]

    applicant_profile = ApplicantProfile(**applicant_profile_response.json())

    position_catalog = get_position_catalog()
    skills_catalog = get_skills_catalog()
    education_catalog = get_education_catalog()
    work_type_catalog = get_work_type_catalog()
    contract_type_catalog = get_contract_type_catalog()

    additional_info = {
        "position": None,
        "skills": [],
        "education_level": None,
        "work_type": None,
        "contract_type": None,
        "seniority_level": 1,  # TODO: implement seniority level #PROJR-60
    }

    for position in position_catalog:
        if position.id == applicant_profile.position_id:
            additional_info["position"] = position

    for skill in skills_catalog:
        if skill.id in applicant_profile.skill_ids:
            additional_info["skills"].append(skill)

    for education in education_catalog:
        if education.id == applicant_profile.education_level_id:
            additional_info["education_level"] = education

    for work_type in work_type_catalog:
        if work_type.id == applicant_profile.work_type_id:
            additional_info["work_type"] = work_type

    for contract_type in contract_type_catalog:
        if contract_type.id == applicant_profile.contract_type_id:
            additional_info["contract_type"] = contract_type

    applicant_profile_dict = applicant_profile.model_dump()
    applicant_profile_dict.update(additional_info)
    hydrated_applicant_profile = ApplicantProfileDTO(**applicant_profile_dict)
    hydrated_applicant_profile.experiences = experiences

    return hydrated_applicant_profile
