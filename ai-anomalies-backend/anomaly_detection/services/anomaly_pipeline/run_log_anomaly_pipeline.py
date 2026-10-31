from dataclasses import dataclass

from ...schemas.processed_log import ProcessedLog
from .data_splitting.split_log_data import split_log_data
from .detect_anomalies import DetectedAnomaly, detect_anomalies
from .model_registration.register_log_anomaly_model import RegisteredModel, register_log_anomaly_model
from .model_training.train_log_anomaly_model import train_log_anomaly_model
from .preprocessing.preprocess_log_file import preprocess_log_file


@dataclass(frozen=True)
class LogAnomalyPipelineResult:
    model: RegisteredModel
    lines_processed: int
    anomalies: list[DetectedAnomaly]


def run_log_anomaly_pipeline(content: str) -> LogAnomalyPipelineResult:
    """Preprocess, split, train, register, and score one uploaded log file."""
    logs: list[ProcessedLog] = preprocess_log_file(content)
    split = split_log_data(logs)
    trained_model = train_log_anomaly_model([log.normalized for log in split.training])
    registered_model = register_log_anomaly_model(
        trained_model,
        training_rows=len(split.training),
        holdout_messages=[log.normalized for log in split.testing],
    )
    anomalies = detect_anomalies(logs, registered_model_uri=registered_model.uri)
    return LogAnomalyPipelineResult(registered_model, len(logs), anomalies)
