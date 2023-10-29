import requests

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from lavoro_library.models import UserInDB, Token
from lavoro_api_gateway.helpers.request_helpers import propagate_response


def get_account(email: str):
    response = requests.get(f"http://auth-api/account/{email}")
    return propagate_response(response, response_model=UserInDB)


def get_token(form_data: OAuth2PasswordRequestForm):
    response = requests.post("http://auth-api/login/token", data=vars(form_data))
    return propagate_response(response, response_model=Token)
