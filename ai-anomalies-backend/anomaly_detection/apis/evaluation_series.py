from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..schemas.model_evaluation import ModelEvaluationSeries
from ..services import get_evaluation_series

router = APIRouter(prefix="/api/v1/model-evaluations", tags=["model evaluations"])


@router.get("/series", response_model=ModelEvaluationSeries)
def get_series(
    limit: Annotated[int, Query(ge=1, le=1000)] = 500,
    model_name: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
) -> ModelEvaluationSeries:
    try:
        return ModelEvaluationSeries(evaluations=get_evaluation_series(limit=limit, model_name=model_name))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Could not retrieve model evaluation series from PostgreSQL.") from exc
