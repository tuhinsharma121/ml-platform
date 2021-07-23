from fastapi import APIRouter, Request
from pydantic import BaseModel

from kronos.cloud_cluster.emr_cluster import EMRCluster

router = APIRouter()


class JobStatusRequest(BaseModel):
    job_id: str


@router.post("/api/v1/kronos/scheduler/job/status",
             tags=["Cluster Status"],
             response_model=dict,
             summary="Cluster Status")
async def get_job_status(app_req: Request, data_req: JobStatusRequest):
    """It checks the status of a cluster/job
    Parameters
    ----------
        app_req : fastapi.Request
            Base request object of Fastapi
        data_req : JobStatusRequest
            request data in json format

    Returns
    -------
        response : dict
            job_id : str
                id of the job
            status : str
                status of the job (success/failed/running)
    """

    status = EMRCluster.get_status_of_cluster_id(cluster_id=data_req.job_id)
    response = dict()
    response["cluster_id"] = data_req.job_id
    response["status"] = status
    return response
