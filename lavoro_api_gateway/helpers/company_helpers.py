import requests
import uuid

from fastapi.encoders import jsonable_encoder

from pydantic import EmailStr

from lavoro_api_gateway.helpers.request_helpers import propagate_response

# from lavoro_library.models import (
#     CompanyInvitation,
#     CreateCompanyRequest,
#     CreateRecruiterProfileRequest,
#     RecruiterProfileInDB,
#     RecruiterProfileWithCompanyName,
#     RecruiterRole,
# )
from lavoro_library.model.company_api.db_models import RecruiterRole
from lavoro_library.model.company_api.dtos import (
    CreateRecruiterProfileWithCompanyDTO,
    CreateCompanyDTO,
    InviteTokenDTO,
    RecruiterProfileDTO,
    RecruiterProfileWithCompanyNameDTO,
)


def create_recruiter_profile(
    payload: CreateRecruiterProfileWithCompanyDTO, account_id: uuid.UUID, recruiter_role: RecruiterRole
):
    response = requests.post(
        f"http://company-api/recruiter/create-recruiter-profile/{account_id}/{recruiter_role}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def get_recruiter_profile(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile/{account_id}")
    return propagate_response(response, response_model=RecruiterProfileDTO)


def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile-with-company-name/{account_id}")
    return propagate_response(response, response_model=RecruiterProfileWithCompanyNameDTO)


def create_company_profile(payload: CreateCompanyDTO, account_id: uuid.UUID):
    response = requests.post(
        f"http://company-api/company/create-company/{account_id}",
        json=jsonable_encoder(payload),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)


def invite_recruiter_to_company(new_recruiter_email: EmailStr, company_id: uuid.UUID):
    response = requests.post(
        f"http://company-api/company/invite-recruiter/{company_id}/{new_recruiter_email}",
    )
    return propagate_response(response)


def check_invite_token(invite_token: str):
    response = requests.get(
        f"http://company-api/recruiter/can-join-company/{invite_token}",
    )  # maybe this should be renamed to get-invite-token rather than can-join-company
    return propagate_response(response, response_model=InviteTokenDTO)


def add_recruiter_to_company(account_id: uuid.UUID, company_id: uuid.UUID):
    response = requests.post(
        f"http://company-api/recruiter/join-company/{company_id}/{account_id}",
    )
    return propagate_response(response)


def delete_invite_token(invite_token: str):
    response = requests.delete(
        f"http://company-api/company/delete-invite-token/{invite_token}",
    )
    return propagate_response(response)
