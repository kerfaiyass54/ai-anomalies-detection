from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..errors import RuntimeCommandError
from ..schemas import PodInfo
from ..services import list_pods

router = APIRouter(prefix="/api/v1/runtime", tags=["runtime inspection"])


@router.get("/pods", response_model=list[PodInfo])
def get_pods(namespace: Annotated[str | None, Query(min_length=1, max_length=253)] = None) -> list[PodInfo]:
    try:
        return list_pods(namespace=namespace)
    except RuntimeCommandError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
