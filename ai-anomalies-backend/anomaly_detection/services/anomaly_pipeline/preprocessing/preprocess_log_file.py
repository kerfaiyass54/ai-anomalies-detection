from ....errors import AnomalyProcessingError
from ....schemas.processed_log import ProcessedLog
from .preprocess_log_line import preprocess_log_line


def preprocess_log_file(content: str) -> list[ProcessedLog]:
    """Parse non-empty lines and normalize variable timestamps and identifiers."""
    processed: list[ProcessedLog] = []
    for raw_line in content.splitlines():
        log = preprocess_log_line(raw_line)
        if log is not None:
            processed.append(log)

    if len(processed) < 4:
        raise AnomalyProcessingError("At least 4 non-empty log lines are required to train and split the model.")
    return processed
