from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse

from ..errors import RuntimeCommandError
from ..services import get_pod_logs

router = APIRouter(prefix="/api/v1/runtime", tags=["runtime inspection"])


@router.get("/pods/{pod_name}/logs", response_class=PlainTextResponse)
def pod_logs(
    pod_name: str,
    namespace: Annotated[str, Query(min_length=1, max_length=253)],
    container: Annotated[str | None, Query(min_length=1, max_length=253)] = None,
    tail: Annotated[int, Query(ge=1, le=10000)] = 200,
) -> str:
    try:
        return get_pod_logs(pod_name, namespace=namespace, container=container, tail=tail)
    except RuntimeCommandError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
