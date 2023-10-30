from fastapi import HTTPException


def propagate_response(response, response_model=None):
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"],
        )
    if response_model is None:
        return response.json()
    return response_model(**response.json())
