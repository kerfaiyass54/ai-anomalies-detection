from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from ..errors import AnomalyProcessingError
from ..schemas.model_evaluation import ModelEvaluation, ModelEvaluationPage, ModelEvaluationRequest
from ..services import evaluate_predictions, list_evaluations

router = APIRouter(prefix="/api/v1/model-evaluations", tags=["model evaluations"])


@router.post("", response_model=ModelEvaluation, status_code=201)
def create_evaluation(request: ModelEvaluationRequest) -> ModelEvaluation:
    try:
        return evaluate_predictions(
            model_name=request.model_name,
            model_version=request.model_version,
            y_true=request.y_true,
            y_pred=request.y_pred,
        )
    except AnomalyProcessingError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Could not calculate or save model evaluation.") from exc


@router.get("", response_model=ModelEvaluationPage)
def get_evaluations(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 50,
    model_name: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
    model_version: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
) -> ModelEvaluationPage:
    try:
        return list_evaluations(page=page, per_page=per_page, model_name=model_name, model_version=model_version)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Could not retrieve model evaluations from PostgreSQL.") from exc
