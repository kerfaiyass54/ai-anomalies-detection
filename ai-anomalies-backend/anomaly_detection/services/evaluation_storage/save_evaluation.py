from sqlalchemy import text

from ...schemas.model_evaluation import ModelEvaluation
from ..anomaly_storage.database import get_database_engine
from .schema import ensure_evaluations_table


def save_evaluation(
    *,
    source_type: str,
    model_name: str,
    model_version: str,
    logs_evaluated: int,
    anomalies_detected: int,
    anomaly_rate: float,
    mean_score: float,
    median_score: float,
    min_score: float,
    max_score: float,
    dataset_sha256: str,
) -> ModelEvaluation:
    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_evaluations_table(connection)
        result = connection.execute(text("""
            INSERT INTO model_evaluations (
                source_type, model_name, model_version, logs_evaluated,
                anomalies_detected, anomaly_rate, mean_score, median_score,
                min_score, max_score, dataset_sha256
            ) VALUES (
                :source_type, :model_name, :model_version, :logs_evaluated,
                :anomalies_detected, :anomaly_rate, :mean_score, :median_score,
                :min_score, :max_score, :dataset_sha256
            )
            RETURNING id, evaluated_at, source_type, model_name, model_version,
                logs_evaluated, anomalies_detected, anomaly_rate, mean_score,
                median_score, min_score, max_score, dataset_sha256
        """), {
            "source_type": source_type,
            "model_name": model_name,
            "model_version": model_version,
            "logs_evaluated": logs_evaluated,
            "anomalies_detected": anomalies_detected,
            "anomaly_rate": anomaly_rate,
            "mean_score": mean_score,
            "median_score": median_score,
            "min_score": min_score,
            "max_score": max_score,
            "dataset_sha256": dataset_sha256,
        })
        return ModelEvaluation(**result.mappings().one())
