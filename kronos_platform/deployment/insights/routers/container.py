import subprocess

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Container(BaseModel):
    container_id: str = None


@router.get("/container/get-id", response_model=Container, tags=["Utils"], summary="Get the container id")
async def get_container_id():
    """Get the container id which is serving the request.

    Returns
    -------
        response : Container
            container_id : str
                id of the container serving the request
    """
    try:
        bash_command = "cat /etc/hostname"
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, _ = process.communicate()
        cid = output.decode("utf-8").strip()
    except Exception as e:
        cid = "localhost"
    response = Container()
    response.container_id = cid
    return response
