import uuid
import requests

from lavoro_api_gateway.helpers.request_helpers import propagate_response
from lavoro_api_gateway.database.queries import (
    get_position_catalog,
    get_skills_catalog,
    get_education_catalog,
    get_work_type_catalog,
    get_contract_type_catalog,
)
from lavoro_library.models import CreateApplicantProfileRequest, ApplicantProfile, ApplicantProfileInDB


def create_applicant_profile(account_id: uuid.UUID, payload: CreateApplicantProfileRequest):
    response = requests.post(
        f"http://applicant-api/applicant/create_applicant_profile/{account_id}",
        json=payload.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def get_applicant_profile(account_id: uuid.UUID):
    response = requests.get(f"http://applicant-api/applicant/get_applicant_profile/{account_id}")
    if response.status_code >= 400:
        propagate_response(response)

    applicant_profile = ApplicantProfileInDB(**response.json())

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
        "seniority_level": "Junior",  # TODO: implement seniority level #PROJR-60
    }

    for position in position_catalog:
        if position.id == applicant_profile.position_id:
            additional_info["position"] = position.position_name

    for skill in skills_catalog:
        if skill.id in applicant_profile.skill_id_list:
            additional_info["skills"].append(skill.skill_name)

    for education in education_catalog:
        if education.id == applicant_profile.education_level_id:
            additional_info["education_level"] = education.education_level

    for work_type in work_type_catalog:
        if work_type.id == applicant_profile.work_type_id:
            additional_info["work_type"] = work_type.work_type

    for contract_type in contract_type_catalog:
        if contract_type.id == applicant_profile.contract_type_id:
            additional_info["contract_type"] = contract_type.contract_type

    full_dict = applicant_profile.model_dump()
    full_dict.update(additional_info)
    hydrated_applicant_profile = ApplicantProfile(**full_dict)

    return hydrated_applicant_profile
