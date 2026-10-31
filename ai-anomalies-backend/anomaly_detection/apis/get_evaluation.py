from fastapi import APIRouter, HTTPException, Path

from ..schemas.model_evaluation import ModelEvaluation
from ..services import get_evaluation

router = APIRouter(prefix="/api/v1/model-evaluations", tags=["model evaluations"])


@router.get("/{evaluation_id}", response_model=ModelEvaluation)
def get_evaluation_by_id(evaluation_id: int = Path(ge=1)) -> ModelEvaluation:
    try:
        evaluation = get_evaluation(evaluation_id)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Could not retrieve the model evaluation from PostgreSQL.") from exc
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Model evaluation was not found.")
    return evaluation
