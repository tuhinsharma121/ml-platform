from typing import List

from fastapi import APIRouter, Request
from pydantic import BaseModel

from kronos_platform.src.forecast_engine.serve_model import load_and_score_forecast_model
from kronos.logging.error_notifier import get_error_stack_trace

router = APIRouter()


class ForecastModelRequest(BaseModel):
    client: str
    item: str
    date_list: List[str]


@router.post("/api/v1/kronos/insights/engines/forecast/score",
             tags=["Forecasting Engine"],
             response_model=dict,
             summary="Forecasting Engine")
async def score_forecast_model(app_req: Request, data_req: ForecastModelRequest):
    """Online inference for forecast model
    Parameters
    ----------
        app_req : fastapi.Request
            Base request object of Fastapi
        data_req : ForecastModelRequest
            request data in json format

    Returns
    -------
        response : dict
            model_name : str
                Name of the model used for scoring
            model_uri : str
                URI of the model managed by mlflow
            result : dict
                Contains the model prediction
    """
    try:
        model_name, model_uri, result = load_and_score_forecast_model(client=data_req.client, item=data_req.item,
                                                                      date_list=data_req.date_list)
        response = dict()
        response["model_name"] = model_name
        response["model_uri"] = model_uri
        response["result"] = result
        return response
    except Exception:
        error_stack_trace = get_error_stack_trace()
        response = dict()
        response["error"] = error_stack_trace
        return response
