from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..errors import KibanaVisualizationServiceError
from ..schemas import KibanaVisualizationPage
from ..services import list_visualizations

router = APIRouter(prefix="/api/v1/kibana/visualizations", tags=["Kibana visualizations"])


@router.get("", response_model=KibanaVisualizationPage)
def get_visualizations(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 100,
    search: Annotated[str | None, Query(min_length=1, max_length=200)] = None,
) -> KibanaVisualizationPage:
    try:
        return list_visualizations(page=page, per_page=per_page, search=search)
    except KibanaVisualizationServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
