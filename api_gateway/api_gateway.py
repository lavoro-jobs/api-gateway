from fastapi import APIRouter, FastAPI

from api_gateway.database.database import db
from api_gateway.routers.auth import router as auth_router


router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)

app = FastAPI()
app.include_router(router)