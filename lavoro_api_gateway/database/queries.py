from typing import List

from lavoro_api_gateway.database import db
from lavoro_library.models import PositionCatalog, EducationCatalog, ContractTypeCatalog, WorkTypeCatalog, SkillsCatalog


def get_position_catalog() -> List[PositionCatalog]:
    result = db.execute_query("SELECT * FROM position_catalog")
    return [PositionCatalog(**position) for position in result["result"]]


def get_skills_catalog() -> List[SkillsCatalog]:
    result = db.execute_query("SELECT * FROM skills_catalog")
    return [SkillsCatalog(**skill) for skill in result["result"]]
    

def get_education_catalog() -> List[EducationCatalog]:
    result = db.execute_query("SELECT * FROM education_catalog")
    return [EducationCatalog(**education) for education in result["result"]]
    

def get_contract_type_catalog() -> List[ContractTypeCatalog]:
    result = db.execute_query("SELECT * FROM contract_type_catalog")
    return [ContractTypeCatalog(**contract_type) for contract_type in result["result"]]
    

def get_work_type_catalog() -> List[WorkTypeCatalog]:
    result = db.execute_query("SELECT * FROM work_type_catalog")
    return [WorkTypeCatalog(**work_type) for work_type in result["result"]]
