import requests
import uuid

from lavoro_api_gateway.helpers.request_helpers import propagate_response
from lavoro_library.models import CreateCompanyRequest, RecruiterProfileInDB, RecruiterProfileWithCompanyName


def create_recruiter_profile(payload, account_id: uuid.UUID):
    response = requests.post(
        f"http://company-api/recruiter/create-recruiter-profile/{account_id}",
        json=payload.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def get_recruiter_profile(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile/{account_id}")
    return propagate_response(response, response_model=RecruiterProfileInDB)


def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile-with-company-name/{account_id}")
    return propagate_response(response, response_model=RecruiterProfileWithCompanyName)


def create_company_profile(payload: CreateCompanyRequest, account_id: uuid.UUID):
    response = requests.post(
        f"http://company-api/company/create-company/{account_id}",
        json=payload.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)
