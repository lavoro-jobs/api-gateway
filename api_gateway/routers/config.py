from fastapi import APIRouter
from api_gateway.database.queries import (
    get_position_catalog,
    get_skills_catalog,
    get_education_catalog,
    get_contract_type_catalog,
    get_work_type_catalog,
)

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/get_positions")
def get_positions():
    result = get_position_catalog()
    return result


@router.get("/get_skills")
def get_skills():
    result = get_skills_catalog()
    return result


@router.get("/get_education")
def get_education():
    result = get_education_catalog()

    return result


@router.get("/get_contract_types")
def get_contract_types():
    result = get_contract_type_catalog()
    return result


@router.get("/get_work_types")
def get_work_types():
    result = get_work_type_catalog()
    return result


@router.get("/get_all_catalogs")
def get_all_catalogs():
    result = {
        "positions": get_position_catalog(),
        "skills": get_skills_catalog(),
        "education": get_education_catalog(),
        "contract_types": get_contract_type_catalog(),
        "work_types": get_work_type_catalog(),
    }
    return result
