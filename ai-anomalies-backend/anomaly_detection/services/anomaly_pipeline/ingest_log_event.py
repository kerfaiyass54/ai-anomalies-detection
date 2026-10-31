from dataclasses import dataclass
from ...schemas.anomaly import AnomalyRecord, LogEvent, LogSourceType
from .model_inference.score_log_event import score_log_event
from .preprocessing.preprocess_log_line import preprocess_log_line
from ...errors import AnomalyProcessingError
from ..anomaly_storage.save_anomalies import save_anomalies


@dataclass(frozen=True)
class LogEventIngestResult:
    model_name: str
    model_version: str
    anomaly: AnomalyRecord | None


def ingest_log_event(event: LogEvent) -> LogEventIngestResult:
    """Preprocess, score, and persist an individual incoming log event."""
    log = preprocess_log_line(event.message, occurred_at=event.occurred_at)
    if log is None:
        raise AnomalyProcessingError("The log event message cannot be empty.")

    model, detected = score_log_event(log)
    saved = save_anomalies([detected], source_type=event.source_type) if detected else []
    return LogEventIngestResult(
        model_name=model.name,
        model_version=model.version,
        anomaly=saved[0] if saved else None,
    )
