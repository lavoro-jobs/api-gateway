from lavoro_api_gateway.database import db


def get_position_catalog():
    result = db.execute_query("SELECT * FROM position_catalog")
    return result["result"]


def get_skills_catalog():
    result = db.execute_query("SELECT * FROM skills_catalog")
    return result["result"]


def get_education_catalog():
    result = db.execute_query("SELECT * FROM education_catalog")
    return result["result"]


def get_contract_type_catalog():
    result = db.execute_query("SELECT * FROM contract_type_catalog")
    return result["result"]


def get_work_type_catalog():
    result = db.execute_query("SELECT * FROM work_type_catalog")
    return result["result"]
