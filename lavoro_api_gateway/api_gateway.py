from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lavoro_api_gateway.routers.auth import router as auth_router
from lavoro_api_gateway.routers.config import router as config_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(config_router)

app.include_router(router)
