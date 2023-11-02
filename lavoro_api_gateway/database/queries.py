from typing import List

from lavoro_api_gateway.database import db
from lavoro_library.models import PositionCatalog, EducationCatalog, ContractTypeCatalog, WorkTypeCatalog, SkillsCatalog


def get_position_catalog() -> List[PositionCatalog]:
    query_tuple = ("SELECT * FROM position_catalog", None)
    result = db.execute_one(query_tuple)
    return [PositionCatalog(**position) for position in result["result"]]


def get_skills_catalog() -> List[SkillsCatalog]:
    query_tuple = ("SELECT * FROM skills_catalog", None)
    result = db.execute_one(query_tuple)
    return [SkillsCatalog(**skill) for skill in result["result"]]


def get_education_catalog() -> List[EducationCatalog]:
    query_tuple = ("SELECT * FROM education_catalog", None)
    result = db.execute_one(query_tuple)
    return [EducationCatalog(**education) for education in result["result"]]


def get_contract_type_catalog() -> List[ContractTypeCatalog]:
    query_tuple = ("SELECT * FROM contract_type_catalog", None)
    result = db.execute_one(query_tuple)
    return [ContractTypeCatalog(**contract_type) for contract_type in result["result"]]


def get_work_type_catalog() -> List[WorkTypeCatalog]:
    query_tuple = ("SELECT * FROM work_type_catalog", None)
    result = db.execute_one(query_tuple)
    return [WorkTypeCatalog(**work_type) for work_type in result["result"]]
