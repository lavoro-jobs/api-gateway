import uuid
import requests
from pydantic import EmailStr

from fastapi import HTTPException

from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.company_api.db_models import RecruiterProfile


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
