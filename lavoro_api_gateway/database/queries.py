from typing import List

from lavoro_api_gateway.database import db
from lavoro_library.models import PositionInDB, SkillInDB, EducationInDB, ContractTypeInDB, WorkTypeInDB


def get_position_catalog():
    query_tuple = ("SELECT * FROM position_catalog", None)
    result = db.execute_one(query_tuple)
    return [PositionInDB(**position) for position in result["result"]]


def get_skills_catalog():
    query_tuple = ("SELECT * FROM skills_catalog", None)
    result = db.execute_one(query_tuple)
    return [SkillInDB(**skill) for skill in result["result"]]


def get_education_catalog():
    query_tuple = ("SELECT * FROM education_catalog", None)
    result = db.execute_one(query_tuple)
    return [EducationInDB(**education) for education in result["result"]]


def get_contract_type_catalog():
    query_tuple = ("SELECT * FROM contract_type_catalog", None)
    result = db.execute_one(query_tuple)
    return [ContractTypeInDB(**contract_type) for contract_type in result["result"]]


def get_work_type_catalog():
    query_tuple = ("SELECT * FROM work_type_catalog", None)
    result = db.execute_one(query_tuple)
    return [WorkTypeInDB(**work_type) for work_type in result["result"]]
