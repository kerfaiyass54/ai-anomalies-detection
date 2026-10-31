from sqlalchemy import text

from ...schemas.model_evaluation import ModelEvaluation
from ..anomaly_storage.database import get_database_engine
from .schema import ensure_evaluations_table


def get_evaluation_series(*, limit: int = 500, source_type: str | None = None) -> list[ModelEvaluation]:
    source_filter = "WHERE source_type = :source_type" if source_type is not None else ""
    params: dict[str, object] = {"limit": limit}
    if source_type is not None:
        params["source_type"] = source_type
    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_evaluations_table(connection)
        rows = connection.execute(text(f"""
            SELECT * FROM (
                SELECT id, evaluated_at, source_type, model_name, model_version,
                    logs_evaluated, anomalies_detected, anomaly_rate, mean_score,
                    median_score, min_score, max_score, dataset_sha256
                FROM model_evaluations
                {source_filter}
                ORDER BY evaluated_at DESC, id DESC
                LIMIT :limit
            ) latest
            ORDER BY evaluated_at ASC, id ASC
        """), params).mappings().all()
    return [ModelEvaluation(**row) for row in rows]
