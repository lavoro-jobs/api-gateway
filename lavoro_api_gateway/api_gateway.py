from fastapi import APIRouter, FastAPI

from lavoro_api_gateway.database import db
from lavoro_api_gateway.routers.auth import router as auth_router
from lavoro_api_gateway.routers.config import router as config_router


router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(config_router)

app = FastAPI()
app.include_router(router)
