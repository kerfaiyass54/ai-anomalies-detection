class AnomalyProcessingError(Exception):
    """A log file could not be processed by the anomaly detection pipeline."""

    def __init__(self, message: str, *, status_code: int = 422) -> None:
        super().__init__(message)
        self.status_code = status_code
