from sqlalchemy import text

from ...schemas.model_evaluation import ModelEvaluation
from ..anomaly_storage.database import get_database_engine
from .schema import ensure_evaluations_table


def get_evaluation(evaluation_id: int) -> ModelEvaluation | None:
    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_evaluations_table(connection)
        row = connection.execute(text("""
            SELECT id, evaluated_at, model_name, model_version,
                samples_evaluated, precision_score AS "precision", recall_score AS "recall",
                f1_score, classification_report, input_sha256
            FROM model_evaluation_metrics
            WHERE id = :evaluation_id
        """), {"evaluation_id": evaluation_id}).mappings().first()
    return ModelEvaluation(**row) if row else None
