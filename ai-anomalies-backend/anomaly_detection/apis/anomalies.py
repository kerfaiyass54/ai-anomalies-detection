from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from ..errors import AnomalyProcessingError
from ..schemas.anomaly import AnomalyDetectionResponse, LogEvent, LogEventIngestResponse, LogSourceType
from ..services import ingest_log_event, run_log_anomaly_pipeline, save_anomalies

router = APIRouter(prefix="/api/v1/anomalies", tags=["anomaly detection"])
MAX_LOG_FILE_BYTES = 10 * 1024 * 1024


@router.post("/detect", response_model=AnomalyDetectionResponse)
async def detect_log_anomalies(
    file: Annotated[UploadFile, File(description="UTF-8 plain text log file")],
    source_type: Annotated[LogSourceType, Query(description="Origin of the uploaded logs")],
) -> AnomalyDetectionResponse:
    if file.filename and not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=415, detail="Upload a .txt log file.")
    content = await file.read(MAX_LOG_FILE_BYTES + 1)
    if len(content) > MAX_LOG_FILE_BYTES:
        raise HTTPException(status_code=413, detail="Log file must be 10 MB or smaller.")
    try:
        text_content = content.decode("utf-8", errors="replace")
        result = run_log_anomaly_pipeline(text_content)
        saved = save_anomalies(result.anomalies, source_type=source_type)
    except AnomalyProcessingError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Anomaly processing failed. Check model registry and database configuration.") from exc
    finally:
        await file.close()

    return AnomalyDetectionResponse(
        model_name=result.model.name,
        model_version=result.model.version,
        lines_processed=result.lines_processed,
        anomalies_saved=len(saved),
        anomalies=saved,
    )


@router.post("/ingest", response_model=LogEventIngestResponse)
def ingest_logstash_event(event: LogEvent) -> LogEventIngestResponse:
    """Score one structured Logstash event with the latest registered model."""
    try:
        result = ingest_log_event(event)
    except AnomalyProcessingError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Log event scoring failed. Check model registry and database configuration.") from exc
    return LogEventIngestResponse(
        model_name=result.model_name,
        model_version=result.model_version,
        anomaly_detected=result.anomaly is not None,
        anomaly=result.anomaly,
    )
