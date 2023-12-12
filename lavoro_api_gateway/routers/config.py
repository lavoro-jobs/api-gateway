from fastapi import APIRouter

from typing import List

from lavoro_api_gateway.services import config_service

from lavoro_library.model.api_gateway.dtos import (
    ContractTypeDTO,
    EducationLevelDTO,
    PositionDTO,
    SkillDTO,
    WorkTypeDTO,
)


router = APIRouter(prefix="/config", tags=["config"])


@router.get("/get-positions", response_model=List[PositionDTO])
def get_positions():
    return config_service.get_position_catalog()


@router.get("/get-skills", response_model=List[SkillDTO])
def get_skills():
    return config_service.get_skills_catalog()


@router.get("/get-education", response_model=List[EducationLevelDTO])
def get_education():
    return config_service.get_education_catalog()


@router.get("/get-contract-types", response_model=List[ContractTypeDTO])
def get_contract_types():
    return config_service.get_contract_type_catalog()


@router.get("/get-work-types", response_model=List[WorkTypeDTO])
def get_work_types():
    return config_service.get_work_type_catalog()


@router.get("/get-all-catalogs")
def get_all_catalogs():
    return {
        "positions": config_service.get_position_catalog(),
        "skills": config_service.get_skills_catalog(),
        "education": config_service.get_education_catalog(),
        "contract_types": config_service.get_contract_type_catalog(),
        "work_types": config_service.get_work_type_catalog(),
    }
