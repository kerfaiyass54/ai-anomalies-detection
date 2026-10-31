from typing import Iterable

from sqlalchemy import text

from ...schemas.anomaly import AnomalyRecord, LogSourceType
from ..anomaly_pipeline.detect_anomalies import DetectedAnomaly
from .database import get_database_engine
from .schema import ensure_anomalies_table


def save_anomalies(anomalies: Iterable[DetectedAnomaly], *, source_type: LogSourceType) -> list[AnomalyRecord]:
    """Persist detected log lines and return their database-assigned identifiers."""
    records = list(anomalies)
    if not records:
        return []

    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_anomalies_table(connection)
        saved = []
        for record in records:
            result = connection.execute(
                text("""
                    INSERT INTO detected_anomalies (occurred_at, source_type, details, score)
                    VALUES (:occurred_at, :source_type, :details, :score)
                    RETURNING id, occurred_at, source_type, details, score
                """),
                {
                    "occurred_at": record.occurred_at,
                    "source_type": source_type,
                    "details": record.details,
                    "score": record.score,
                },
            )
            saved.append(AnomalyRecord(**result.mappings().one()))

    return saved
