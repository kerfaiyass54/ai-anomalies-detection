from sqlalchemy import text

from ...schemas.model_evaluation import ModelEvaluation
from ..anomaly_storage.database import get_database_engine
from .schema import ensure_evaluations_table


def get_evaluation_series(*, limit: int = 500, model_name: str | None = None) -> list[ModelEvaluation]:
    model_filter = "WHERE model_name = :model_name" if model_name is not None else ""
    params: dict[str, object] = {"limit": limit}
    if model_name is not None:
        params["model_name"] = model_name
    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_evaluations_table(connection)
        rows = connection.execute(text(f"""
            SELECT * FROM (
                SELECT id, evaluated_at, model_name, model_version,
                    samples_evaluated, precision_score AS "precision", recall_score AS "recall",
                    f1_score, classification_report, input_sha256
                FROM model_evaluation_metrics
                {model_filter}
                ORDER BY evaluated_at DESC, id DESC
                LIMIT :limit
            ) latest
            ORDER BY evaluated_at ASC, id ASC
        """), params).mappings().all()
    return [ModelEvaluation(**row) for row in rows]
