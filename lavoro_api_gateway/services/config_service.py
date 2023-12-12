from lavoro_api_gateway.database import queries


def get_position_catalog():
    return queries.get_position_catalog()


def get_skills_catalog():
    return queries.get_skills_catalog()


def get_education_catalog():
    return queries.get_education_catalog()


def get_contract_type_catalog():
    return queries.get_contract_type_catalog()


def get_work_type_catalog():
    return queries.get_work_type_catalog()
