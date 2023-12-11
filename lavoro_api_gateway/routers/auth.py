from typing import Annotated

from fastapi import APIRouter, Depends, Response

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_active_user
from lavoro_api_gateway.helpers.auth_helpers import get_token, confirm_email_with_token, register_user
from lavoro_api_gateway.services import auth_service


# from lavoro_library.models import LoginForm, RegistrationForm, Token, User
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.auth_api.dtos import AccountDTO, LoginDTO, RegisterDTO, TokenDTO


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenDTO)
def login(response: Response, form_data: Annotated[LoginDTO, Depends()]):
    token_data = auth_service.login(form_data)
    # token_data = get_token(form_data)
    if token_data:
        response.set_cookie(key="access_token", value=f"Bearer {token_data.access_token}", httponly=True)
    return token_data


@router.get("/account/current", response_model=AccountDTO)
def get_current_account(current_user: Annotated[AccountDTO, Depends(get_current_active_user)]):
    return current_user


@router.post("/register")
def register(form_data: Annotated[RegisterDTO, Depends()]):
    return auth_service.register(form_data)
    # return register_user(form_data)


@router.post("/register/confirm/{verification_token}")
def confirm_email(verification_token: str):
    return auth_service.confirm_email(verification_token)
    # confirmation_result = confirm_email_with_token(verification_token)
    # return confirmation_result
