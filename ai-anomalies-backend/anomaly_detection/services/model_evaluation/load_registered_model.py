import os
from functools import lru_cache

import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
from sklearn.pipeline import Pipeline

from ...errors import AnomalyProcessingError


def _configure_mlflow() -> tuple[str, str]:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///./mlflow.db")
    model_name = os.getenv("MLFLOW_ANOMALY_MODEL_NAME", "log-anomaly-detector")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_registry_uri(tracking_uri)
    return model_name, tracking_uri


@lru_cache(maxsize=8)
def _load_model(model_uri: str) -> Pipeline:
    return mlflow.sklearn.load_model(model_uri)


def load_registered_model(version: str | None = None) -> tuple[str, str, Pipeline]:
    model_name, _ = _configure_mlflow()
    client = MlflowClient()
    versions = [
        item for item in client.search_model_versions(f"name='{model_name}'")
        if item.status == "READY"
    ]
    if not versions:
        raise AnomalyProcessingError(
            "No trained anomaly model is registered yet. Train a model by uploading a log file first.",
            status_code=503,
        )

    if version is None:
        selected = max(versions, key=lambda item: int(item.version))
    else:
        selected = next((item for item in versions if item.version == version), None)
        if selected is None:
            raise AnomalyProcessingError(
                f"Model version '{version}' is not registered and ready.", status_code=404
            )

    model_uri = f"models:/{model_name}/{selected.version}"
    return model_name, str(selected.version), _load_model(model_uri)
