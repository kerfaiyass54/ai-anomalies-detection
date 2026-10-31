import os
from dataclasses import dataclass

import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
from sklearn.pipeline import Pipeline


@dataclass(frozen=True)
class RegisteredModel:
    name: str
    version: str
    uri: str


def register_log_anomaly_model(
    model: Pipeline, *, training_rows: int, holdout_messages: list[str]
) -> RegisteredModel:
    """Log and register the fitted pipeline in the configured MLflow registry."""
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///./mlflow.db")
    model_name = os.getenv("MLFLOW_ANOMALY_MODEL_NAME", "log-anomaly-detector")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_registry_uri(tracking_uri)
    mlflow.set_experiment("log-anomaly-detection")

    with mlflow.start_run() as run:
        holdout_predictions = model.predict(holdout_messages)
        mlflow.log_param("algorithm", "IsolationForest")
        mlflow.log_param("training_rows", training_rows)
        mlflow.log_param("holdout_rows", len(holdout_messages))
        mlflow.log_param("feature_extractor", "character_tfidf_2_to_5_grams")
        mlflow.log_metric(
            "holdout_anomaly_rate",
            float((holdout_predictions == -1).mean()),
        )
        mlflow.sklearn.log_model(model, artifact_path="model")
        model_uri = f"runs:/{run.info.run_id}/model"

    registered = mlflow.register_model(model_uri=model_uri, name=model_name)
    MlflowClient().set_model_version_tag(model_name, registered.version, "training_rows", str(training_rows))
    return RegisteredModel(name=model_name, version=str(registered.version), uri=f"models:/{model_name}/{registered.version}")
