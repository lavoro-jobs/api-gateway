from fastapi import APIRouter

from typing import List

from lavoro_api_gateway.database.queries import (
    get_position_catalog,
    get_skills_catalog,
    get_education_catalog,
    get_contract_type_catalog,
    get_work_type_catalog,
)

from lavoro_library.models import (
    PositionCatalog,
    EducationCatalog,
    ContractTypeCatalog,
    WorkTypeCatalog,
    SkillsCatalog,
)


router = APIRouter(prefix="/config", tags=["config"])


@router.get("/get_positions", response_model=List[PositionCatalog])
def get_positions():
    result = get_position_catalog()
    return result


@router.get("/get_skills", response_model=List[SkillsCatalog])
def get_skills():
    result = get_skills_catalog()
    return result


@router.get("/get_education", response_model=List[EducationCatalog])
def get_education():
    result = get_education_catalog()
    return result


@router.get("/get_contract_types", response_model=List[ContractTypeCatalog])
def get_contract_types():
    result = get_contract_type_catalog()
    return result


@router.get("/get_work_types", response_model=List[WorkTypeCatalog])
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
