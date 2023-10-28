import requests
from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
def login():
    response = requests.get("http://auth-api/login/")
    return response
