import logging

import mysql.connector as connector

from config import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER
from kronos.data_store.abstract_data_store import AbstractDataStore


class MySQLDataStore(AbstractDataStore):
    def __init__(self):
        self.__create_connection()

    def __create_connection(self):
        self.__host = MYSQL_HOST
        self.__user = MYSQL_USER
        self.__password = MYSQL_PASSWORD
        self.__conn = connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password)
        return None

    def __run_sql_to_get_data(self, query):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            cursor_des = cursor.description
            cursor.close()
            return records, cursor_des
        except Exception as e:
            logging.exception(e)
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
            logging.exception(e)
            self.__create_connection()
            return None

    def run_custom_select_sql(self, query):
        records, cursor_des = self.__run_sql_to_get_data(query=query)
        return records, cursor_des

    def run_custom_update_sql(self, query):
        return self.__run_sql_to_push_data(query=query)

    def close_connection(self):
        self.__conn.close()
