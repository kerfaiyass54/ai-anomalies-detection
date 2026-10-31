from .command import run_command


def get_container_logs(container_id: str, *, tail: int = 200) -> str:
    """Return recent logs for a Docker container ID or name."""
    return run_command(["docker", "logs", "--tail", str(tail), "--", container_id], include_stderr=True)
