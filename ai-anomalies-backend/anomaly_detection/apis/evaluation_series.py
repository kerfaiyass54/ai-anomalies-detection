from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..schemas.anomaly import LogSourceType
from ..schemas.model_evaluation import ModelEvaluationSeries
from ..services import get_evaluation_series

router = APIRouter(prefix="/api/v1/model-evaluations", tags=["model evaluations"])


@router.get("/series", response_model=ModelEvaluationSeries)
def get_series(
    limit: Annotated[int, Query(ge=1, le=1000)] = 500,
    source_type: Annotated[LogSourceType | None, Query()] = None,
) -> ModelEvaluationSeries:
    try:
        return ModelEvaluationSeries(evaluations=get_evaluation_series(limit=limit, source_type=source_type))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Could not retrieve model evaluation series from PostgreSQL.") from exc
