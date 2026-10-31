from fastapi import APIRouter, HTTPException

from ..errors import RuntimeCommandError
from ..schemas import ContainerInfo
from ..services import list_containers

router = APIRouter(prefix="/api/v1/runtime", tags=["runtime inspection"])


@router.get("/containers", response_model=list[ContainerInfo])
def get_containers() -> list[ContainerInfo]:
    try:
        return list_containers()
    except RuntimeCommandError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
