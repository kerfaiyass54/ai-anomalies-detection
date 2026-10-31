from sqlalchemy import text

from ...schemas.model_evaluation import ModelEvaluation, ModelEvaluationPage
from ..anomaly_storage.database import get_database_engine
from .schema import ensure_evaluations_table


def list_evaluations(
    *, page: int = 1, per_page: int = 100, model_name: str | None = None, model_version: str | None = None
) -> ModelEvaluationPage:
    filters: list[str] = []
    params: dict[str, object] = {"limit": per_page, "offset": (page - 1) * per_page}
    if model_name is not None:
        filters.append("model_name = :model_name")
        params["model_name"] = model_name
    if model_version is not None:
        filters.append("model_version = :model_version")
        params["model_version"] = model_version
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    filter_params = {key: value for key, value in params.items() if key not in {"limit", "offset"}}

    engine = get_database_engine()
    with engine.begin() as connection:
        ensure_evaluations_table(connection)
        total = connection.execute(
            text(f"SELECT COUNT(*) FROM model_evaluation_metrics {where_clause}"), filter_params
        ).scalar_one()
        rows = connection.execute(text(f"""
            SELECT id, evaluated_at, model_name, model_version,
                samples_evaluated, precision_score AS "precision", recall_score AS "recall",
                f1_score, classification_report, input_sha256
            FROM model_evaluation_metrics
            {where_clause}
            ORDER BY evaluated_at DESC, id DESC
            LIMIT :limit OFFSET :offset
        """), params).mappings().all()

    return ModelEvaluationPage(
        page=page, per_page=per_page, total=total,
        evaluations=[ModelEvaluation(**row) for row in rows],
    )
