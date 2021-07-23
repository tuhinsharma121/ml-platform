from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HeartbeatResponse(BaseModel):
    message: str = None


@router.get("/", tags=["Utils"], response_model=HeartbeatResponse, summary="Heartbeat")
async def index():
    """heartbeat

    Returns
    -------
        response : HeartbeatResponse
            message : str
                Message from the server
    """
    response = dict()
    response["message"] = "Ninja always kicks!!!"
    return response
