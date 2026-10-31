from sqlalchemy import text

from ...schemas.model_evaluation import ModelEvaluation
from ..anomaly_storage.database import get_database_engine
from .schema import ensure_evaluations_table


def get_evaluation(evaluation_id: int) -> ModelEvaluation | None:
    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_evaluations_table(connection)
        row = connection.execute(text("""
            SELECT id, evaluated_at, source_type, model_name, model_version,
                logs_evaluated, anomalies_detected, anomaly_rate, mean_score,
                median_score, min_score, max_score, dataset_sha256
            FROM model_evaluations
            WHERE id = :evaluation_id
        """), {"evaluation_id": evaluation_id}).mappings().first()
    return ModelEvaluation(**row) if row else None
