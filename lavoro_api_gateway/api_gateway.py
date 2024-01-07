from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lavoro_api_gateway.routers.applicant import router as applicant_router
from lavoro_api_gateway.routers.auth import router as auth_router
from lavoro_api_gateway.routers.company import router as company_router
from lavoro_api_gateway.routers.config import router as config_router
from lavoro_api_gateway.routers.matches import router as matches_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://lavoro-frontend.azurewebsites.net", "https://lavorojobs.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter(prefix="/api/v1")
router.include_router(applicant_router)
router.include_router(auth_router)
router.include_router(company_router)
router.include_router(config_router)
router.include_router(matches_router)


app.include_router(router)
