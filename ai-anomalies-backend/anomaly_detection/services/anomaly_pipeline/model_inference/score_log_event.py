import os
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache

import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
from sklearn.pipeline import Pipeline

from ....errors import AnomalyProcessingError
from ....schemas.processed_log import ProcessedLog
from ..detect_anomalies import DetectedAnomaly


@dataclass(frozen=True)
class RegisteredModelReference:
    name: str
    version: str
    uri: str


@lru_cache(maxsize=8)
def _load_model(model_uri: str) -> Pipeline:
    return mlflow.sklearn.load_model(model_uri)


def _latest_registered_model() -> RegisteredModelReference:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///./mlflow.db")
    model_name = os.getenv("MLFLOW_ANOMALY_MODEL_NAME", "log-anomaly-detector")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_registry_uri(tracking_uri)

    client = MlflowClient()
    versions = [
        version for version in client.search_model_versions(f"name='{model_name}'")
        if version.status == "READY"
    ]
    if not versions:
        raise AnomalyProcessingError(
            "No trained anomaly model is registered yet. Train a model by uploading a log file first.",
            status_code=503,
        )
    latest = max(versions, key=lambda version: int(version.version))
    return RegisteredModelReference(
        name=model_name,
        version=str(latest.version),
        uri=f"models:/{model_name}/{latest.version}",
    )


def score_log_event(log: ProcessedLog) -> tuple[RegisteredModelReference, DetectedAnomaly | None]:
    """Score one Logstash event using the latest ready registered model."""
    registered_model = _latest_registered_model()
    model = _load_model(registered_model.uri)
    prediction = model.predict([log.normalized])[0]
    if prediction != -1:
        return registered_model, None

    score = float(model.decision_function([log.normalized])[0])
    return registered_model, DetectedAnomaly(
        occurred_at=log.occurred_at,
        details=log.original,
        score=score,
    )
