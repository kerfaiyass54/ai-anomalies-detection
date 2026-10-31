class RuntimeCommandError(Exception):
    """A local Docker or Kubernetes CLI command could not be completed."""

    def __init__(self, message: str, *, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code
