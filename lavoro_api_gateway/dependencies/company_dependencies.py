from typing import Annotated

from fastapi import Depends, HTTPException

from lavoro_api_gateway import common
from lavoro_api_gateway.dependencies.auth_dependencies import get_current_recruiter_user

from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.company_api.db_models import RecruiterProfile


def get_recruiter_profile(current_user: Annotated[Account, Depends(get_current_recruiter_user)]):
    return common.get_recruiter_profile(current_user.id)


def get_admin_recruiter_profile(recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)]):
    if recruiter_profile.recruiter_role != "admin":
        raise HTTPException(status_code=403, detail="User is not a company admin")
    return recruiter_profile


def get_recruiter_job_posts(recruiter_profile: Annotated[RecruiterProfile, Depends(get_recruiter_profile)]):
    if recruiter_profile.recruiter_role != "admin":
        return common.get_recruiter_job_posts(recruiter_profile.account_id)
    return common.get_job_posts_by_company(recruiter_profile.company_id)
