import requests

from fastapi.encoders import jsonable_encoder

from lavoro_api_gateway.helpers.request_helpers import propagate_response
from lavoro_library.models import LoginForm, RegistrationForm, Token, UserInDB


def get_account(email: str):
    response = requests.get(f"http://auth-api/account/{email}")
    return propagate_response(response, response_model=UserInDB)


def get_token(form_data: LoginForm):
    response = requests.post("http://auth-api/login/token", data=jsonable_encoder(form_data))
    return propagate_response(response, response_model=Token)


def register_user(form_data: RegistrationForm):
    response = requests.post("http://auth-api/register", data=jsonable_encoder(form_data))
    return propagate_response(response)


def confirm_email_with_token(verification_token: str):
    response = requests.post(f"http://auth-api/register/confirm/{verification_token}")
    return propagate_response(response)
