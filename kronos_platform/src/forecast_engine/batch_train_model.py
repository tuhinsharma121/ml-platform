import argparse
import json

import pandas as pd

from kronos_platform.schemas.forecast_engine.input_schema import ForecastDataSchema
from kronos_platform.src.forecast_engine.model.prophet_model import ProphetModel
from kronos.data_store.snowflake_data_store import SnowflakeDataStore
from kronos.engine_manager.schema_manager import SchemaManager
from kronos.logging import pylogger
from kronos.logging.error_notifier import *

logger = pylogger.configure_logger(name="kronos_logger", log_path="/tmp/train_forecast.log")


def main():
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("--client", required=True)
        ap.add_argument("--params", required=True)

        args = vars(ap.parse_args())

        client = args["client"]
        params_str = args["params"]

        model_params = None
        if params_str is not None:
            model_params = json.loads(params_str)

        logger.info("client : {client}".format(client=client))
        logger.info("model params : {model_params}".format(model_params=model_params))

        sf_data_store = SnowflakeDataStore()
        data = SchemaManager.get_schema(company="INTEL", data_store=None)
        forecast_schema = ForecastDataSchema(client=data["client"], db=data["db"], schema=data["schema"],
                                             table=data["table"], item_id=data["item_id"], month=data["month"],
                                             year=data["year"], day=data["day"], target=data["target"],
                                             item_list=data["item_list"], prediction=data["prediction"])

        for item in forecast_schema.item_list:
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
            records = sf_data_store.run_custom_select_sql(sql)

            cols = [
                forecast_schema.item_id,
                forecast_schema.month,
                forecast_schema.year,
                forecast_schema.target
            ]
            df = pd.DataFrame(records)
            df.columns = cols

            df[forecast_schema.month] = df[forecast_schema.month].map(lambda x: "{0:0=2d}".format(int(x)))
            df = df.astype({forecast_schema.year: str, forecast_schema.month: str})
            df['ds'] = df[forecast_schema.year] + "-" + df[forecast_schema.month] + "-" + '01'
            df["y"] = df[forecast_schema.target]
            df = df[df["y"] > 0]

            model, params, metrics = ProphetModel.train(df, model_params)

            experiment_name = "{client}-{engine}-{item}".format(engine="forecast", client=forecast_schema.client,
                                                                item=item)
            model.save(params=params, metrics=metrics, experiment_name=experiment_name)

    except Exception as e:
        stack_trace = get_error_stack_trace()
        logger.exception(stack_trace)
        send_notification(message=stack_trace)
        raise


if __name__ == "__main__":
    main()
