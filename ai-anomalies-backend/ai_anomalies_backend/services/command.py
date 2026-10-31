import os
import shutil
import subprocess

from ..errors import RuntimeCommandError


def run_command(command: list[str], *, include_stderr: bool = False, timeout: int = 30) -> str:
    executable = shutil.which(command[0])
    if executable is None:
        raise RuntimeCommandError(
            f"Required executable '{command[0]}' is not installed or not on PATH.",
            status_code=503,
        )
    command[0] = executable
    try:
        result = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if include_stderr else subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=False,
            env=os.environ.copy(),
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeCommandError(
            f"'{os.path.basename(executable)}' did not finish within {timeout} seconds.",
            status_code=504,
        ) from exc
    except OSError as exc:
        raise RuntimeCommandError(f"Could not run '{os.path.basename(executable)}'.", status_code=503) from exc

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "Command failed."
        raise RuntimeCommandError(detail[:2000])
    return result.stdout
