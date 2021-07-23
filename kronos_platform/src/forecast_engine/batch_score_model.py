import argparse
import json

import mlflow
import pyspark.sql.functions as sf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import struct
from pyspark.sql.types import *

from kronos_platform.schemas.forecast_engine.input_schema import ForecastDataSchema
from kronos_platform.src.forecast_engine.model.prophet_model import ProphetModel
from kronos.engine_manager.schema_manager import SchemaManager
from kronos.logging import pylogger
from kronos.logging.error_notifier import *

logger = pylogger.configure_logger(name="kronos_logger", log_path="/tmp/score_forecast.log")


def main():
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("--client", required=True)
        ap.add_argument("--params", required=True)

        args = vars(ap.parse_args())

        client = args["client"]
        params_str = args["params"]

        params = None
        if params_str is not None:
            params = json.loads(params_str)

        logger.info("client : {client}".format(client=client))
        logger.info("params : {model_params}".format(model_params=params))

        spark = SparkSession.builder.getOrCreate()

        sf_options = {
            "sfUrl": SF_ACCOUNT + ".snowflakecomputing.com",
            "sfUser": SF_USER,
            "sfPassword": SF_PASSWORD,
            "sfDatabase": "DEV_INTEL",
            "sfWarehouse": SF_WAREHOUSE,
            "truncate_table": "ON",
            "usestagingtable": "OFF",
        }

        data = SchemaManager.get_schema(company="INTEL", data_store=None)
        forecast_schema = ForecastDataSchema(client=data["client"], db=data["db"], schema=data["schema"],
                                             table=data["table"], item_id=data["item_id"], month=data["month"],
                                             year=data["year"], day=data["day"], target=data["target"],
                                             item_list=data["item_list"], prediction=data["prediction"])

        for item in forecast_schema.item_list:
            experiment_name = "{client}-{engine}-{item}".format(engine="forecast", client=forecast_schema.client,
                                                                item=item)
            model, model_name, model_uri = ProphetModel.load(experiment_name=experiment_name,
                                                             stage=MLFLOW_DEPLOYMENT_TYPE)

            sql = """
            SELECT
                {item_id},
                {month},
                {year},
                SUM({target}) AS {target}
            FROM {db}.{schema}.{table}
            WHERE {item_id} in ('{item}')
            GROUP BY 
                {item_id},
                {year},
                {month}    
            """.format(item_id=forecast_schema.item_id, month=forecast_schema.month, year=forecast_schema.year,
                       target=forecast_schema.target, db=forecast_schema.db, schema=forecast_schema.schema,
                       table=forecast_schema.table, item=item)

            df = spark.read \
                .format("snowflake") \
                .options(**sf_options) \
                .option("query", sql) \
                .load()

            df.show(4)
            df.printSchema()

            df = df.withColumn("INT", df[forecast_schema.month].cast(IntegerType()))
            df = df.withColumn("STR", sf.format_string("%02d", "INT"))
            df = df.withColumn('ds', sf.concat(sf.col('YEAR'), sf.lit('-'), sf.col('STR'), sf.lit('-01')))

            model_udf = mlflow.pyfunc.spark_udf(spark, model_uri)
            result_sdf = df.withColumn(forecast_schema.prediction, model_udf(struct("ds")))

            result_sdf = result_sdf.withColumn('LOAD_TIME', F.current_timestamp())
            result_sdf = result_sdf.select(forecast_schema.item_id, forecast_schema.month,
                                           forecast_schema.year, forecast_schema.target,
                                           "HX_SO_PC_UNITS_IA", "LOAD_TIME")
            result_sdf.show(3)
            result_sdf.printSchema()

            sf_options_ml = {
                "sfUrl": SF_ACCOUNT + ".snowflakecomputing.com",
                "sfUser": SF_USER,
                "sfPassword": SF_PASSWORD,
                "sfDatabase": "DEV_INTEL_ML",
                "sfSchema": "PUBLIC",
                "sfWarehouse": SF_WAREHOUSE,
                "truncate_table": "ON",
                "usestagingtable": "OFF",
            }

            result_sdf.write.format("snowflake") \
                .options(**sf_options_ml) \
                .mode("append") \
                .option("dbtable", "stg_prediction") \
                .save()

    except Exception as e:
        stack_trace = get_error_stack_trace()
        logger.exception(stack_trace)
        send_notification(message=stack_trace)
        raise


if __name__ == "__main__":
    main()
