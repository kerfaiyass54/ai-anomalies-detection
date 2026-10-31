from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..errors import LogSearchError
from ..schemas import LogSearchPage
from ..services import search_logs

router = APIRouter(prefix="/api/v1/logs", tags=["Elasticsearch logs"])


@router.get("", response_model=LogSearchPage)
def get_logs(
    size: Annotated[int, Query(ge=1, le=1000)] = 100,
    cursor: Annotated[str | None, Query(max_length=4096)] = None,
) -> LogSearchPage:
    try:
        return search_logs(size=size, cursor=cursor)
    except LogSearchError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
