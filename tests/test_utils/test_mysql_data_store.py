from unittest import TestCase

from config import *
from kronos.data_store.mysql_data_store import MySQLDataStore

TABLE = "temp_table"


class TestMySQLDataStore(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMySQLDataStore, self).__init__(*args, **kwargs)
        self.data_store = MySQLDataStore()

    def setUp(self) -> None:
        self.data_store.run_custom_update_sql("DROP DATABASE if exists {db}".format(db=MYSQL_DATABASE))
        self.data_store.run_custom_update_sql("CREATE DATABASE IF NOT EXISTS {db}".format(db=MYSQL_DATABASE))

    def tearDown(self) -> None:
        pass

    def __create_temp_table(self):
        query = """CREATE TABLE {db}.{table} (
                            eid integer, 
                            name varchar(100) 
                            )
                        """.format(db=MYSQL_DATABASE, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)
        response = self.data_store.run_custom_select_sql(
            query="SELECT table_name FROM information_schema.tables WHERE table_schema = '{database}'".format(
                database=MYSQL_DATABASE))
        result = response[0][0][0]
        expected_result = "temp_table"
        self.assertEqual(first=result, second=expected_result)

    def __create_temp_table_with_data(self):
        self.__create_temp_table()
        query = """
                    INSERT INTO {db}.{table} (eid, name) VALUES 
                    (123, 'name_1'), 
                    (456, 'name_2')
                """.format(db=MYSQL_DATABASE, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)

    def test_create_table(self):
        self.__create_temp_table()

    def test_push_data_from_csv(self):
        self.__create_temp_table_with_data()

    def test_run_custom_update_sql(self):
        self.__create_temp_table_with_data()
        query = """
                    UPDATE {db}.{table}
                    SET eid = 789
                    WHERE eid = 123
                """.format(db=MYSQL_DATABASE, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)

        query = """
                   SELECT *
                   FROM {db}.{table}
                """.format(db=MYSQL_DATABASE, table=TABLE)
        result, description = self.data_store.run_custom_select_sql(query=query)
        expected_result = [(789, 'name_1'), (456, 'name_2')]
        self.assertCountEqual(first=result, second=expected_result)

    def test_run_custom_select_sql(self):
        self.__create_temp_table_with_data()
        query = """
                   SELECT *
                   FROM {db}.{table}
                """.format(db=MYSQL_DATABASE, table=TABLE)
        result, description = self.data_store.run_custom_select_sql(query=query)
        expected_result = [(123, 'name_1'), (456, 'name_2')]
        self.assertListEqual(list1=result, list2=expected_result)
