from lavoro_api_gateway.database import db


from lavoro_library.model.api_gateway.dtos import (
    ContractTypeDTO,
    EducationLevelDTO,
    PositionDTO,
    SkillDTO,
    WorkTypeDTO,
)


def get_position_catalog():
    query_tuple = ("SELECT * FROM position_catalog", None)
    result = db.execute_one(query_tuple)
    return [PositionDTO(**position) for position in result["result"]]


def get_skills_catalog():
    query_tuple = ("SELECT * FROM skills_catalog", None)
    result = db.execute_one(query_tuple)
    return [SkillDTO(**skill) for skill in result["result"]]


def get_education_catalog():
    query_tuple = ("SELECT * FROM education_catalog", None)
    result = db.execute_one(query_tuple)
    return [EducationLevelDTO(**education) for education in result["result"]]


def get_contract_type_catalog():
    query_tuple = ("SELECT * FROM contract_type_catalog", None)
    result = db.execute_one(query_tuple)
    return [ContractTypeDTO(**contract_type) for contract_type in result["result"]]


def get_work_type_catalog():
    query_tuple = ("SELECT * FROM work_type_catalog", None)
    result = db.execute_one(query_tuple)
    return [WorkTypeDTO(**work_type) for work_type in result["result"]]
