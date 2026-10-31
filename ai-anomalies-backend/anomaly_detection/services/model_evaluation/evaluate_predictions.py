import hashlib
import json

from sklearn.metrics import classification_report

from ...errors import AnomalyProcessingError
from ...schemas.model_evaluation import ModelEvaluation
from ..evaluation_storage.save_evaluation import save_evaluation


def evaluate_predictions(
    *, model_name: str, model_version: str, y_true: list[int], y_pred: list[int]
) -> ModelEvaluation:
    if not y_true or not y_pred:
        raise AnomalyProcessingError("y_true and y_pred must not be empty.", status_code=422)
    if len(y_true) != len(y_pred):
        raise AnomalyProcessingError("y_true and y_pred must have the same number of labels.", status_code=422)
    if any(type(label) is not int or label not in (0, 1) for label in [*y_true, *y_pred]):
        raise AnomalyProcessingError("Labels must be binary integers: 0 (normal) or 1 (anomaly).", status_code=422)

    report = classification_report(
        y_true,
        y_pred,
        labels=[0, 1],
        target_names=["normal", "anomaly"],
        output_dict=True,
        zero_division=0,
    )
    anomaly_metrics = report["anomaly"]
    input_sha256 = hashlib.sha256(
        json.dumps({"y_true": y_true, "y_pred": y_pred}, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return save_evaluation(
        model_name=model_name,
        model_version=model_version,
        samples_evaluated=len(y_true),
        precision=float(anomaly_metrics["precision"]),
        recall=float(anomaly_metrics["recall"]),
        f1_score=float(anomaly_metrics["f1-score"]),
        classification_report=report,
        input_sha256=input_sha256,
    )
