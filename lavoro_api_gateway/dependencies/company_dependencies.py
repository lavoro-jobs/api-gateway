from typing import Annotated

from fastapi import Depends

from lavoro_api_gateway import common
from lavoro_api_gateway.dependencies.auth_dependencies import get_current_recruiter_user

from lavoro_library.model.auth_api.db_models import Account


def get_recruiter_profile(current_user: Annotated[Account, Depends(get_current_recruiter_user)]):
    return common.get_recruiter_profile(current_user.id)
