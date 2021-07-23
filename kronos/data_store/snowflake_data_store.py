import snowflake.connector

from config import (SF_ACCOUNT, SF_PASSWORD, SF_USER,
                    SF_WAREHOUSE)
from kronos.data_store.abstract_data_store import AbstractDataStore


class SnowflakeDataStore(AbstractDataStore):

    def __init__(self):
        self.__create_connection()

    def __create_connection(self):

        self.__account = SF_ACCOUNT
        self.__user = SF_USER
        self.__password = SF_PASSWORD
        self.__warehouse = SF_WAREHOUSE
        self.__conn = snowflake.connector.connect(
            account=self.__account,
            user=self.__user,
            password=self.__password,
            warehouse=self.__warehouse
        )
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
        except Exception:
            self.__create_connection()
            return None

    def run_custom_update_sql(self, query):
        mobile_records = self.__run_sql_to_push_data(query=query)
        return mobile_records

    def run_custom_select_sql(self, query):
        return self.__run_sql_to_get_data(query=query)

    def close_connection(self):
        self.__conn.close()
