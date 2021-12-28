import logging
from typing import Optional, List, Any

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor


class DbConnector:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_port = db_port
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.connection = self.__create_connection()

    def __del__(self):
        if self.connection:
            self.connection.close()
            logging.info("Disconnected from PostgreSQL")

    def execute(self, query: str):
        self.__execute(query)

    def select(self, query: str) -> Optional[List[Any]]:
        cursor = self.__execute(query, True)
        try:
            return cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            return []
        finally:
            if self.connection:
                cursor.close()

    def __execute(self, query: str, _return: bool = False) -> Optional[RealDictCursor]:
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query)
            logging.debug("Query executed successfully")
        except OperationalError as e:
            logging.error(f"The error '{e}' occurred")
        finally:
            if self.connection and not _return:
                cursor.close()
        if _return:
            return cursor

    def __create_connection(self):
        connection = None
        try:
            connection = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
            connection.autocommit = True
            logging.info("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            logging.error(f"The error '{e}' occurred")
        return connection
