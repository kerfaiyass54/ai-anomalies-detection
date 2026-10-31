from ...schemas.model_retraining import ModelRetrainingResponse
from ..anomaly_pipeline.data_splitting.split_log_data import split_log_data
from ..anomaly_pipeline.model_registration.register_log_anomaly_model import register_log_anomaly_model
from ..anomaly_pipeline.model_training.train_log_anomaly_model import train_log_anomaly_model
from ..anomaly_pipeline.preprocessing.preprocess_log_file import preprocess_log_file


def retrain_model(content: str) -> ModelRetrainingResponse:
    """Fit and register a new Isolation Forest version from a fresh log file."""
    logs = preprocess_log_file(content)
    split = split_log_data(logs)
    model = train_log_anomaly_model([log.normalized for log in split.training])
    registered = register_log_anomaly_model(
        model,
        training_rows=len(split.training),
        holdout_messages=[log.normalized for log in split.testing],
    )
    return ModelRetrainingResponse(
        model_name=registered.name,
        model_version=registered.version,
        training_rows=len(split.training),
        holdout_rows=len(split.testing),
    )
