import logging
import os
import sys
import time
import psycopg2

from fastapi.logger import logger as fastapi_logger


logger = logging.getLogger("gunicorn.error")

class Database:
    def __init__(self):
        self.connection = self.connect()

    def connect(self, max_retries=3):
        connection_string = os.environ.get("CONFIG_DATABASE_CONNECTION_STRING")
        for i in range(0, max_retries):
            try:
                connection = psycopg2.connect(connection_string)
                return connection
            except psycopg2.OperationalError as e:
                print("Unable to connect to config database. Retrying...")
                time.sleep(3)
        print("Unable to connect to config database")
        sys.exit(1)


db = Database()