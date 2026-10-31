import re
from datetime import datetime, timezone

from ....errors import AnomalyProcessingError
from ....schemas.processed_log import ProcessedLog

_TIMESTAMP = re.compile(
    r"^\[?(?P<timestamp>\d{4}-\d{2}-\d{2}[T ][0-9:.+-]+(?:Z)?)\]?\s*"
)
_UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F-]{27,}\b")
_IP_ADDRESS = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_NUMBER = re.compile(r"\b\d+\b")


def preprocess_log_file(content: str) -> list[ProcessedLog]:
    """Parse non-empty lines and normalize variable timestamps and identifiers."""
    processed: list[ProcessedLog] = []
    for raw_line in content.splitlines():
        original = raw_line.strip()
        if not original:
            continue

        occurred_at = datetime.now(timezone.utc)
        match = _TIMESTAMP.match(original)
        message = original
        if match:
            timestamp = match.group("timestamp").replace("Z", "+00:00")
            try:
                occurred_at = datetime.fromisoformat(timestamp)
                if occurred_at.tzinfo is None:
                    occurred_at = occurred_at.replace(tzinfo=timezone.utc)
                message = original[match.end():].strip()
            except ValueError:
                pass

        normalized = _UUID.sub("<UUID>", message)
        normalized = _IP_ADDRESS.sub("<IP>", normalized)
        normalized = _NUMBER.sub("<NUM>", normalized)
        if normalized:
            processed.append(ProcessedLog(original, normalized, occurred_at))

    if len(processed) < 4:
        raise AnomalyProcessingError("At least 4 non-empty log lines are required to train and split the model.")
    return processed
