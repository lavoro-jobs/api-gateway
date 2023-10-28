import os
import sys
import time
import psycopg2


class Database:
    def __init__(self, connection_string):
        self.connection = self.connect(connection_string)

    def connect(self, connection_string, max_retries=3):
        for i in range(0, max_retries):
            try:
                connection = psycopg2.connect(connection_string)
                return connection
            except psycopg2.OperationalError as e:
                print("Unable to connect to config database. Retrying...")
                time.sleep(3)
        print("Unable to connect to config database")
        sys.exit(1)


db = Database(os.environ.get("DB_CONNECTION_STRING"))
