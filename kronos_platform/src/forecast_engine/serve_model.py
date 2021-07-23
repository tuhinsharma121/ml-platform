import argparse

import pandas as pd

from kronos_platform.schemas.forecast_engine.input_schema import ForecastDataSchema
from kronos_platform.src.forecast_engine.model.prophet_model import ProphetModel
from kronos.engine_manager.schema_manager import SchemaManager
from kronos.logging import pylogger
from kronos.logging.error_notifier import get_error_stack_trace, send_notification
from config import *

logger = pylogger.configure_logger(name="kronos_logger", log_path="/tmp/toy_trains.log")


def load_and_score_forecast_model(client, item, date_list):
    """Loads model from mlflow and score the model against the input data

    Parameters
    ----------
    client : str
        client name
    item : str
        name of the item for which to calculate the forecast
    date_list : List[str]
        list of the dates for which forecast needs to be calculated

    Returns
    -------
    model_name : str
        name of the model in mlflow
    model_uri : str
        model uri in mlflow including model version
    result : dict
        forecast data in (date,forecast) key-value pair format
    """
    experiment_name = "{client}-{engine}-{item}".format(engine="forecast", client=client,
                                                        item=item)
    model, model_name, model_uri = ProphetModel.load(experiment_name=experiment_name, stage=MLFLOW_DEPLOYMENT_TYPE)
    test_df = pd.DataFrame(date_list, columns=["ds"])
    forecast_df = model.predict(test_df)
    result = dict(zip(test_df["ds"], forecast_df["yhat"]))
    return model_name, model_uri, result


def main():
    try:
        data = SchemaManager.get_schema(company="INTEL", data_store=None)
        forecast_schema = ForecastDataSchema(client=data["client"], db=data["db"], schema=data["schema"],
                                             table=data["table"], item_id=data["item_id"],
                                             prediction=data["prediction"],
                                             month=data["month"],
                                             year=data["year"], day=data["day"], target=data["target"],
                                             item_list=data["item_list"])

        date_list = ["2021-04-01", "2021-05-01", "2021-06-01"]
        for item in forecast_schema.item_list:
            model_name, model_uri, result = load_and_score_forecast_model(client=forecast_schema.client,
                                                                          item=item,
                                                                          date_list=date_list)
            logger.info(result)

    except Exception as e:
        stack_trace = get_error_stack_trace()
        logger.exception(stack_trace)
        send_notification(message=stack_trace)


if __name__ == "__main__":
    main()
