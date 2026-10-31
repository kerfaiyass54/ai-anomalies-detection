from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse

from ..errors import RuntimeCommandError
from ..services import get_container_logs

router = APIRouter(prefix="/api/v1/runtime", tags=["runtime inspection"])


@router.get("/containers/{container_id}/logs", response_class=PlainTextResponse)
def container_logs(container_id: str, tail: Annotated[int, Query(ge=1, le=10000)] = 200) -> str:
    try:
        return get_container_logs(container_id, tail=tail)
    except RuntimeCommandError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
