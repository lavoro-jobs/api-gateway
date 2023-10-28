from api_gateway.database.database import db

def get_config():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM config")
    config = cursor.fetchone()
    cursor.close()
    return config