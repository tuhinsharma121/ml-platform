class SchemaManager(object):
    def __init__(self, **kwargs):
        super(SchemaManager, self).__init__(**kwargs)

    @classmethod
    def get_schema(cls, company, data_store):
        # result = data_store.run_custom_sql(company)
        result = {"client": "INTEL",
                  "db": "DEV_INTEL",
                  "schema": "PUBLIC",
                  "table": "STG_OLAP_INTEL",
                  "item_id": "PROCESSOR_GROUP",
                  "month": "MONTH_NO",
                  "year": "YEAR",
                  "target": "SO_PC_UNITS_IA",
                  "prediction": "HX_SO_PC_UNITS_IA",
                  "day": None,
                  "item_list": ["Celeron", "Intel", "Core", "Pentium"]}

        return result