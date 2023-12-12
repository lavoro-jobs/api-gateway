import os

from typing import Annotated

from typing import Optional, Dict

from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param


from lavoro_api_gateway import common

from lavoro_library.model.company_api.db_models import RecruiterRole
from lavoro_library.model.auth_api.db_models import Role
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.auth_api.dtos import TokenDataDTO


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/login")

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenDataDTO(email=email)
    except JWTError:
        raise credentials_exception
    user = common.get_account(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[Account, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_applicant_user(current_user: Annotated[Account, Depends(get_current_active_user)]):
    if not current_user.role == Role.applicant:
        raise HTTPException(status_code=400, detail="User is not an applicant")
    return current_user


def get_current_recruiter_user(current_user: Annotated[Account, Depends(get_current_active_user)]):
    if not current_user.role == Role.recruiter:
        raise HTTPException(status_code=400, detail="User is not a recruiter")
    return current_user


def get_current_company_admin_user(current_user: Annotated[Account, Depends(get_current_recruiter_user)]):
    """
    There are two cases when this function will "pass" and return the current_user:
    1. The current_user has an account role of "recruiter" and a recruiter_role of "admin"
    2. The current_user has an account role of "recruiter" and doesn't have a recruiter_profile,
    which means they haven't created a recruiter profile yet. This is the case when a recruiter
    first registers with the system, but still has to create a recruiter profile
    """

    try:
        recruiter_profile = common.get_recruiter_profile(current_user.id)
    except HTTPException:
        recruiter_profile = None

    if not recruiter_profile or recruiter_profile.recruiter_role == RecruiterRole.admin:
        return current_user

    raise HTTPException(status_code=400, detail="User is not a company admin")
