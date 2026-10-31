from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..errors import AnomalyProcessingError
from ..schemas.model_retraining import ModelRetrainingResponse
from ..services import retrain_model

router = APIRouter(prefix="/api/v1/models", tags=["model management"])
MAX_RETRAINING_FILE_BYTES = 10 * 1024 * 1024


@router.post("/retrain", response_model=ModelRetrainingResponse, status_code=201)
async def retrain_anomaly_model(
    file: Annotated[UploadFile, File(description="UTF-8 plain text file containing fresh training logs")],
) -> ModelRetrainingResponse:
    try:
        if file.filename and not file.filename.lower().endswith(".txt"):
            raise HTTPException(status_code=415, detail="Upload a .txt log file.")
        content = await file.read(MAX_RETRAINING_FILE_BYTES + 1)
        if len(content) > MAX_RETRAINING_FILE_BYTES:
            raise HTTPException(status_code=413, detail="Training file must be 10 MB or smaller.")
        return retrain_model(content.decode("utf-8", errors="replace"))
    except AnomalyProcessingError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Model retraining failed. Check model registry configuration.",
        ) from exc
    finally:
        await file.close()
