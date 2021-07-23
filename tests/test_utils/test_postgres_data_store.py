from unittest import TestCase

from config import *
from kronos.data_store.postgres_data_store import PostgresDataStore

SCHEMA = "test_schema"
DB_NAME = POSTGRES_DB
TABLE = "temp_table"


class TestPostgresDataStore(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPostgresDataStore, self).__init__(*args, **kwargs)
        self.data_store = PostgresDataStore()

    def setUp(self):
        self.data_store.run_custom_update_sql("drop schema if exists {schema} cascade".format(schema=SCHEMA))
        self.data_store.run_custom_update_sql("create schema if not exists {schema}".format(schema=SCHEMA))

    def tearDown(self):
        pass

    def __create_temp_table(self):
        query = \
            """
                CREATE TABLE {db}.{schema}.{table} (
                eid integer, 
                name varchar(100) 
                )
            """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)
        response = self.data_store.run_custom_select_sql(
            query="SELECT tablename FROM pg_tables WHERE schemaname = '{schema}'".format(schema=SCHEMA))
        result = response[0][0]
        expected_result = "temp_table"
        self.assertEqual(first=result, second=expected_result)

    def __create_temp_table_with_data(self):
        self.__create_temp_table()
        query = \
            """
                INSERT INTO {db}.{schema}.{table} (eid, name) VALUES 
                (123, 'name_1'), 
                (456, 'name_2')
            """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)

    def test_create_table(self):
        self.__create_temp_table()

    def test_push_data_from_csv(self):
        self.__create_temp_table_with_data()

    def test_run_custom_update_sql(self):
        self.__create_temp_table_with_data()
        query = \
            """
                UPDATE {db}.{schema}.{table}
                SET eid = 789
                WHERE eid = 123
            """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)

        query = \
            """
               SELECT * 
               FROM {db}.{schema}.{table}
            """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_select_sql(query=query)
        expected_result = [(789, 'name_1'), (456, 'name_2')]
        self.assertCountEqual(first=result, second=expected_result)

    def test_run_custom_select_sql(self):
        self.__create_temp_table_with_data()
        query = \
            """
               SELECT * 
               FROM {db}.{schema}.{table}
            """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_select_sql(query=query)
        expected_result = [(123, 'name_1'), (456, 'name_2')]
        self.assertListEqual(list1=result, list2=expected_result)
