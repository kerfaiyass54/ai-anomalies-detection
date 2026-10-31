from dataclasses import dataclass
from datetime import datetime

import mlflow.sklearn
from sklearn.pipeline import Pipeline

from ...schemas.processed_log import ProcessedLog


@dataclass(frozen=True)
class DetectedAnomaly:
    occurred_at: datetime
    details: str
    score: float


def detect_anomalies(logs: list[ProcessedLog], *, registered_model_uri: str) -> list[DetectedAnomaly]:
    """Load the registered model and identify anomalous lines in the input file."""
    model: Pipeline = mlflow.sklearn.load_model(registered_model_uri)
    predictions = model.predict([log.normalized for log in logs])
    scores = model.decision_function([log.normalized for log in logs])
    return [
        DetectedAnomaly(occurred_at=log.occurred_at, details=log.original, score=float(score))
        for log, prediction, score in zip(logs, predictions, scores)
        if prediction == -1
    ]
