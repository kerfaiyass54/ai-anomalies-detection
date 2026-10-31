from .command import run_command


def get_pod_logs(
    pod_name: str, *, namespace: str, container: str | None = None, tail: int = 200
) -> str:
    """Return recent logs for a pod in the requested namespace."""
    command = ["kubectl", "logs", "--namespace", namespace, "--tail", str(tail)]
    if container:
        command.extend(["--container", container])
    command.extend(["--", pod_name])
    return run_command(command, include_stderr=True)
