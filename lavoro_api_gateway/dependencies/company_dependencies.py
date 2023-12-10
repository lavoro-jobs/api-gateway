import requests

from typing import Annotated

from fastapi import Depends

from lavoro_api_gateway.dependencies.auth_dependencies import get_current_recruiter_user
from lavoro_api_gateway.helpers.request_helpers import propagate_response

# from lavoro_library.models import UserInDB, RecruiterProfileInDB
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.company_api.db_models import RecruiterProfile


def get_recruiter_profile(current_user: Annotated[Account, Depends(get_current_recruiter_user)]):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile/{current_user.id}")
    return propagate_response(response, response_model=RecruiterProfile)
