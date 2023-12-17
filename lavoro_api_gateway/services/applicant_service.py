import uuid
from typing import List

import requests

from fastapi.encoders import jsonable_encoder

from lavoro_api_gateway.common import (
    fill_database_model_with_catalog_data,
    propagate_response,
    generate_applicant_profile_to_match,
    publish_item_to_match,
)

from lavoro_library.model.applicant_api.dtos import (
    ApplicantProfileDTO,
    CreateApplicantProfileWithExperiencesDTO,
    CreateExperienceDTO,
    ExperienceDTO,
    UpdateApplicantExperienceDTO,
    UpdateApplicantProfileDTO,
)
from lavoro_library.model.applicant_api.db_models import ApplicantProfile, Experience


def create_applicant_profile(account_id: uuid.UUID, payload: CreateApplicantProfileWithExperiencesDTO):
    create_applicant_profile_dto = payload.model_dump(exclude={"experiences"})

    applicant_profile_response = requests.post(
        f"http://applicant-api/applicant/create-applicant-profile/{account_id}",
        json=jsonable_encoder(create_applicant_profile_dto),
        headers={"Content-Type": "application/json"},
    )
    applicant_profile = propagate_response(applicant_profile_response, response_model=ApplicantProfile)

    experiences = []
    if payload.experiences:
        create_experiences_dto = payload.experiences
        experiences_response = requests.post(
            f"http://applicant-api/applicant/create-experiences/{account_id}",
            json=jsonable_encoder(create_experiences_dto),
            headers={"Content-Type": "application/json"},
        )
        experiences = propagate_response(experiences_response)
        experiences = [Experience(**experience) for experience in experiences]

    message = generate_applicant_profile_to_match(applicant_profile, experiences)
    publish_item_to_match(message)

    return {"detail": "Applicant profile created"}


def create_experiences(account_id: uuid.UUID, payload: List[CreateExperienceDTO]):
    response = requests.post(
        f"http://applicant-api/applicant/create-experiences/{account_id}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    propagate_response(response)
    return {"detail": "Applicant experiences created"}


def get_applicant_profile(account_id: uuid.UUID):
    applicant_profile_response = requests.get(f"http://applicant-api/applicant/get-applicant-profile/{account_id}")
    applicant_profile = propagate_response(applicant_profile_response, response_model=ApplicantProfile)

    experiences_response = requests.get(f"http://applicant-api/applicant/get-experiences/{account_id}")
    experiences = propagate_response(experiences_response)

    hydrated_applicant_profile: ApplicantProfileDTO = fill_database_model_with_catalog_data(
        applicant_profile, ApplicantProfileDTO
    )
    hydrated_experiences: List[ExperienceDTO] = []
    for experience in experiences:
        hydrated_experience = fill_database_model_with_catalog_data(Experience(**experience), ExperienceDTO)
        hydrated_experiences.append(hydrated_experience)

    hydrated_applicant_profile.experiences = hydrated_experiences

    return hydrated_applicant_profile


def update_applicant_profile(account_id: uuid.UUID, payload: UpdateApplicantProfileDTO):
    response = requests.patch(
        f"http://applicant-api/applicant/update-applicant-profile/{account_id}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def update_applicant_experience(experience_id: uuid.UUID, payload: UpdateApplicantExperienceDTO):
    response = requests.patch(
        f"http://applicant-api/applicant/update-applicant-experience/{experience_id}", json=jsonable_encoder(payload)
    )
    if response.status_code >= 400:
        propagate_response(response)
    return response.json()


def delete_applicant_experience(experience_id: uuid.UUID):
    response = requests.delete(f"http://applicant-api/applicant/delete-applicant-experience/{experience_id}")
    if response.status_code >= 400:
        propagate_response(response)
    return response.json()
