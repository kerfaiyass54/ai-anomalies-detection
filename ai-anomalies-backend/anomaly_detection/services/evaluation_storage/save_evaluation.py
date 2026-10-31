import json

from sqlalchemy import text

from ...schemas.model_evaluation import ModelEvaluation
from ..anomaly_storage.database import get_database_engine
from .schema import ensure_evaluations_table


def save_evaluation(
    *, model_name: str, model_version: str, samples_evaluated: int,
    precision: float, recall: float, f1_score: float,
    classification_report: dict[str, object], input_sha256: str,
) -> ModelEvaluation:
    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_evaluations_table(connection)
        result = connection.execute(text("""
            INSERT INTO model_evaluation_metrics (
                model_name, model_version, samples_evaluated, precision_score,
                recall_score, f1_score, classification_report, input_sha256
            ) VALUES (
                :model_name, :model_version, :samples_evaluated, :precision,
                :recall, :f1_score, CAST(:classification_report AS JSONB), :input_sha256
            )
            RETURNING id, evaluated_at, model_name, model_version, samples_evaluated,
                precision_score AS "precision", recall_score AS "recall",
                f1_score, classification_report, input_sha256
        """), {
            "model_name": model_name,
            "model_version": model_version,
            "samples_evaluated": samples_evaluated,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "classification_report": json.dumps(classification_report),
            "input_sha256": input_sha256,
        })
        return ModelEvaluation(**result.mappings().one())
