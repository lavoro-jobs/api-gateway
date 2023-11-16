import uuid
import requests

from lavoro_api_gateway.helpers.request_helpers import propagate_response
from lavoro_library.models import CreateApplicantProfileRequest


def create_applicant_profile(account_id: uuid.UUID, payload: CreateApplicantProfileRequest):
    response = requests.post(
        f"http://applicant-api/applicant/create_applicant_profile/{account_id}",
        json=payload.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    return propagate_response(response)
