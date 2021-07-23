from fastapi import APIRouter, Request
from pydantic import BaseModel

from kronos.logging.error_notifier import get_error_stack_trace
from kronos_platform.scripts.forecast_engine.submit_score import submit_scoring_job
from kronos_platform.scripts.forecast_engine.submit_train import submit_training_job

router = APIRouter()


class ForecastTrainRequest(BaseModel):
    client: str
    params: dict


class ForecastScoreRequest(BaseModel):
    client: str
    params: dict


@router.post("/api/v1/kronos/scheduler/engines/forecast/batch-train",
             tags=["Forecasting Engine"],
             response_model=dict,
             summary="Forecasting Engine")
async def train_forecast_model(app_req: Request, data_req: ForecastTrainRequest):
    """Submits a job in cluster for training forecast model in batch mode

    Parameters
    ----------
        app_req : fastapi.Request
            Base request object of Fastapi
        data_req : ForecastTrainRequest
            request data in json format

    Returns
    -------
        On success
            response : dict
                job_id : str
                    id of the submitted job
                status : str
                    status of the job (success/failed/running)

        On exception
            response : dict
                error : str
                    stacktrace of the error

    Raises
    ------
    Exception
        If submitting job to the cluster fails.
    """

    try:
        job_id, status = submit_training_job(client=data_req.client, params=data_req.params)
        response = dict()
        response["job_id"] = job_id
        response["status"] = status
        return response
    except Exception:
        error_stack_trace = get_error_stack_trace()
        response = dict()
        response["error"] = error_stack_trace
        return response


@router.post("/api/v1/kronos/scheduler/engines/forecast/batch-score",
             tags=["Forecasting Engine"],
             response_model=dict,
             summary="Forecasting Engine")
async def score_forecast_model(app_req: Request, data_req: ForecastScoreRequest):
    """Submits a job in cluster for scoring forecast model in batch mode

    Parameters
    ----------
        app_req : fastapi.Request
            Base request object of Fastapi
        data_req : ForecastScoreRequest
            request data in json format

    Returns
    -------
        On success
            response : dict
                job_id : str
                    id of the submitted job
                status : str
                    status of the job (success/failed/running)

        On exception
            response : dict
                error : str
                    stacktrace of the error

    Raises
    ------
    Exception
        If submitting job to the cluster fails.
    """

    try:
        job_id, status = submit_scoring_job(client=data_req.client, params=data_req.params)
        response = dict()
        response["job_id"] = job_id
        response["status"] = status
        return response
    except Exception:
        error_stack_trace = get_error_stack_trace()
        response = dict()
        response["error"] = error_stack_trace
        return response
