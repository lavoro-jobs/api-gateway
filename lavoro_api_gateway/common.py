from typing import List
import uuid
import requests
from pydantic import EmailStr

from fastapi import HTTPException

from lavoro_api_gateway.database.queries import (
    get_position_catalog,
    get_skills_catalog,
    get_education_catalog,
    get_contract_type_catalog,
    get_work_type_catalog,
)
from lavoro_library.model.api_gateway.dtos import ContractTypeDTO, EducationLevelDTO, PositionDTO, SkillDTO, WorkTypeDTO
from lavoro_library.model.auth_api.db_models import Account
from lavoro_library.model.company_api.db_models import RecruiterProfile


def propagate_response(response, response_model=None):
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"],
        )
    if response_model is None:
        return response.json()
    return response_model(**response.json())


def get_account(email: EmailStr):
    response = requests.get(f"http://auth-api/account/{email}")
    return propagate_response(response, response_model=Account)


def get_recruiter_profile(account_id: uuid.UUID):
    response = requests.get(f"http://company-api/recruiter/get-recruiter-profile/{account_id}")
    return propagate_response(response, response_model=RecruiterProfile)


def fill_database_model_with_catalog_data(input_model, output_model_type):
    position_catalog = get_position_catalog()
    skills_catalog = get_skills_catalog()
    education_catalog = get_education_catalog()
    work_type_catalog = get_work_type_catalog()
    contract_type_catalog = get_contract_type_catalog()

    catalog_list = [
        {
            "name_in_db_model": "position_id",
            "name_in_dto": "position",
            "catalog": position_catalog,
            "dto_model": PositionDTO,
            "is_list": False,
        },
        {
            "name_in_db_model": "skill_ids",
            "name_in_dto": "skills",
            "catalog": skills_catalog,
            "dto_model": SkillDTO,
            "is_list": True,
        },
        {
            "name_in_db_model": "education_level_id",
            "name_in_dto": "education_level",
            "catalog": education_catalog,
            "dto_model": EducationLevelDTO,
            "is_list": False,
        },
        {
            "name_in_db_model": "work_type_id",
            "name_in_dto": "work_type",
            "catalog": work_type_catalog,
            "dto_model": WorkTypeDTO,
            "is_list": False,
        },
        {
            "name_in_db_model": "contract_type_id",
            "name_in_dto": "contract_type",
            "catalog": contract_type_catalog,
            "dto_model": ContractTypeDTO,
            "is_list": False,
        },
    ]

    output_dict = input_model.dict()

    for catalog in catalog_list:
        id_field_in_db_model = catalog["name_in_db_model"]
        dto_field_in_output_model = catalog["name_in_dto"]
        catalog_data = catalog["catalog"]
        dto_model = catalog["dto_model"]

        if id_field_in_db_model in input_model.dict():
            if catalog["is_list"] == False:
                id_value = getattr(input_model, id_field_in_db_model)
                corresponding_dto = next((dto for dto in catalog_data if dto.id == id_value), None)
            else:
                id_value_list = getattr(input_model, id_field_in_db_model)
                corresponding_dto = [dto for dto in catalog_data if dto.id in id_value_list]

            if corresponding_dto is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid {id_field_in_db_model} value: {id_value}",
                )

            if catalog["is_list"] == False:
                field = dto_model(**corresponding_dto.dict())
            else:
                field = [dto_model(**dto.dict()) for dto in corresponding_dto]

            output_dict[dto_field_in_output_model] = field

    output_model = output_model_type(**output_dict)

    return output_model
