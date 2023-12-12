import requests

from fastapi.encoders import jsonable_encoder

from lavoro_api_gateway.common import propagate_response
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.auth_api.dtos import LoginDTO, RegisterDTO, TokenDTO


def register(form_data: RegisterDTO):
    response = requests.post("http://auth-api/register", data=jsonable_encoder(form_data))
    return propagate_response(response)


def register_no_confirm(form_data: RegisterDTO):
    response = requests.post("http://auth-api/register/no-confirm", data=jsonable_encoder(form_data))
    return propagate_response(response)


def confirm_email(verification_token: str):
    response = requests.post(f"http://auth-api/register/confirm/{verification_token}")
    return propagate_response(response)


def login(form_data: LoginDTO):
    response = requests.post("http://auth-api/login/token", data=jsonable_encoder(form_data))
    return propagate_response(response, response_model=TokenDTO)
