import psycopg2

from config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT,
                    POSTGRES_USER)
from kronos.data_store.abstract_data_store import AbstractDataStore


class PostgresDataStore(AbstractDataStore):
    def __init__(self):
        self.__create_connection()

    def __create_connection(self):

        self.__host = POSTGRES_HOST
        self.__port = POSTGRES_PORT
        self.__dbname = POSTGRES_DB
        self.__user = POSTGRES_USER
        self.__password = POSTGRES_PASSWORD
        self.__conn = psycopg2.connect(
            host=self.__host,
            port=self.__port,
            dbname=self.__dbname,
            user=self.__user,
            password=self.__password)
        return None

    def __run_sql_to_get_data(self, query):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            self.__conn.commit()
            mobile_records = cursor.fetchall()
            cursor.close()
            return mobile_records
        except Exception:
            self.__create_connection()
            return None

    def __run_sql_to_push_data(self, query):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            self.__conn.commit()
            cursor.close()
            return True
        except Exception as e:
            self.__create_connection()
            return None

    def run_custom_select_sql(self, query):
        mobile_records = self.__run_sql_to_get_data(query=query)
        return mobile_records

    def run_custom_update_sql(self, query):
        return self.__run_sql_to_push_data(query=query)

    def close_connection(self):
        self.__conn.close()
