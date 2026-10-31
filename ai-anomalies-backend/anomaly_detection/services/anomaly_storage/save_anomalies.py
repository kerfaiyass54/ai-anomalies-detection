from typing import Iterable

from sqlalchemy import text

from ...schemas.anomaly import AnomalyRecord, LogSourceType
from ..anomaly_pipeline.detect_anomalies import DetectedAnomaly
from .database import get_database_engine


def save_anomalies(anomalies: Iterable[DetectedAnomaly], *, source_type: LogSourceType) -> list[AnomalyRecord]:
    """Persist detected log lines and return their database-assigned identifiers."""
    records = list(anomalies)
    if not records:
        return []

    engine = get_database_engine()
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS detected_anomalies (
                id BIGSERIAL PRIMARY KEY,
                occurred_at TIMESTAMPTZ NOT NULL,
                source_type VARCHAR(16) NOT NULL CHECK (source_type IN ('k8s', 'docker', 'jenkins')),
                details TEXT NOT NULL,
                score DOUBLE PRECISION NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """))
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
