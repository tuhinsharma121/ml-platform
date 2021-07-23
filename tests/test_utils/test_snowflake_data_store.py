from unittest import TestCase

from kronos.data_store.snowflake_data_store import SnowflakeDataStore

DB_NAME = "TEST_INTEL_DB"
SCHEMA = "TEST_SCHEMA"
TABLE = "TEMP_TABLE"


class TestSnowflakeDataStore(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSnowflakeDataStore, self).__init__(*args, **kwargs)
        self.data_store = SnowflakeDataStore()

    def setUp(self):
        self.data_store.run_custom_update_sql(
            "drop schema if exists {db}.{schema}".format(db=DB_NAME, schema=SCHEMA))
        self.data_store.run_custom_update_sql(
            "create schema if not exists {db}.{schema}".format(db=DB_NAME, schema=SCHEMA))

    def tearDown(self):
        pass

    def __create_temp_table(self):
        query = """
                    CREATE TABLE {db}.{schema}.{table} (
                    eid integer,
                    name varchar(100)
                    )
                """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)
        response = self.data_store.run_custom_select_sql(
            query="SHOW TABLES IN {db}.{schema}".format(db=DB_NAME, schema=SCHEMA))
        result = response[0][1]
        expected_result = TABLE
        self.assertEqual(first=result, second=expected_result)

    def __create_temp_table_with_data(self):
        self.__create_temp_table()
        query = """
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
        query = """
                    UPDATE {db}.{schema}.{table}
                    SET eid = 789
                    WHERE eid = 123
                """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_update_sql(query=query)
        expected_result = True
        self.assertEqual(first=result, second=expected_result)

        query = """
                   SELECT *
                   FROM {db}.{schema}.{table}
                """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_select_sql(query=query)
        expected_result = [(789, 'name_1'), (456, 'name_2')]
        self.assertCountEqual(first=result, second=expected_result)

    def test_run_custom_select_sql(self):
        self.__create_temp_table_with_data()
        query = """
                   SELECT *
                   FROM {db}.{schema}.{table}
                """.format(db=DB_NAME, schema=SCHEMA, table=TABLE)
        result = self.data_store.run_custom_select_sql(query=query)
        expected_result = [(123, 'name_1'), (456, 'name_2')]
        self.assertCountEqual(first=result, second=expected_result)
