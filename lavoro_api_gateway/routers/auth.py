from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_active_user
from lavoro_api_gateway.helpers.auth_helpers import get_token, confirm_email_with_token, register_user
from lavoro_library.models import User, Token, RegistrationForm


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token_data = get_token(form_data)
    return token_data


@router.get("/account/current", response_model=User)
def get_current_account(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post("/register")
def register(form_data: Annotated[RegistrationForm, Depends()]):
    return register_user(form_data)


@router.post("/register/confirm/{verification_token}")
def confirm_email(verification_token: str):
    confirmation_result = confirm_email_with_token(verification_token)
    return confirmation_result
