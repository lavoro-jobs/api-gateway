from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from lavoro_api_gateway.routers.applicant import router as applicant_router
from lavoro_api_gateway.routers.auth import router as auth_router
from lavoro_api_gateway.routers.config import router as config_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter(prefix="/api/v1")
router.include_router(applicant_router)
router.include_router(auth_router)
router.include_router(config_router)

app.include_router(router)
