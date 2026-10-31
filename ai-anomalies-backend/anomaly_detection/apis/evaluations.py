from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from ..errors import AnomalyProcessingError
from ..schemas.anomaly import LogSourceType
from ..schemas.model_evaluation import ModelEvaluation, ModelEvaluationPage
from ..services import evaluate_log_file, list_evaluations

router = APIRouter(prefix="/api/v1/model-evaluations", tags=["model evaluations"])
MAX_EVALUATION_FILE_BYTES = 10 * 1024 * 1024


@router.post("", response_model=ModelEvaluation, status_code=201)
async def create_evaluation(
    file: Annotated[UploadFile, File(description="UTF-8 plain text log file to evaluate")],
    source_type: Annotated[LogSourceType, Query(description="Origin of the evaluated logs")],
    model_version: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
) -> ModelEvaluation:
    if file.filename and not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=415, detail="Upload a .txt log file.")
    content = await file.read(MAX_EVALUATION_FILE_BYTES + 1)
    if len(content) > MAX_EVALUATION_FILE_BYTES:
        raise HTTPException(status_code=413, detail="Evaluation file must be 10 MB or smaller.")
    try:
        return evaluate_log_file(content.decode("utf-8", errors="replace"), source_type=source_type, model_version=model_version)
    except AnomalyProcessingError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Model evaluation failed. Check model registry and database configuration.") from exc
    finally:
        await file.close()


@router.get("", response_model=ModelEvaluationPage)
def get_evaluations(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 50,
    source_type: Annotated[LogSourceType | None, Query()] = None,
    model_version: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
) -> ModelEvaluationPage:
    try:
        return list_evaluations(page=page, per_page=per_page, source_type=source_type, model_version=model_version)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Could not retrieve model evaluations from PostgreSQL.") from exc
