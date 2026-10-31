import hashlib
from statistics import mean, median

from ...errors import AnomalyProcessingError
from ...schemas.anomaly import LogSourceType
from ...schemas.model_evaluation import ModelEvaluation
from ..anomaly_pipeline.preprocessing.preprocess_log_line import preprocess_log_line
from ..evaluation_storage.save_evaluation import save_evaluation
from .load_registered_model import load_registered_model


def evaluate_log_file(
    content: str, *, source_type: LogSourceType, model_version: str | None = None
) -> ModelEvaluation:
    logs = [processed for line in content.splitlines() if (processed := preprocess_log_line(line)) is not None]
    if not logs:
        raise AnomalyProcessingError("The evaluation file must contain at least one non-empty log line.", status_code=422)

    model_name, selected_version, model = load_registered_model(model_version)
    messages = [log.normalized for log in logs]
    predictions = model.predict(messages)
    scores = [float(score) for score in model.decision_function(messages)]
    anomaly_count = int((predictions == -1).sum())

    return save_evaluation(
        source_type=source_type,
        model_name=model_name,
        model_version=selected_version,
        logs_evaluated=len(logs),
        anomalies_detected=anomaly_count,
        anomaly_rate=anomaly_count / len(logs),
        mean_score=mean(scores),
        median_score=median(scores),
        min_score=min(scores),
        max_score=max(scores),
        dataset_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )
