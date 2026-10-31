import json
from typing import Any

from ..errors import RuntimeCommandError
from ..schemas import ContainerInfo
from .command import run_command


def list_containers() -> list[ContainerInfo]:
    """List all Docker containers, including stopped containers."""
    output = run_command(["docker", "ps", "--all", "--no-trunc", "--format", "{{json .}}"])
    containers: list[ContainerInfo] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        try:
            item: dict[str, Any] = json.loads(line)
            state = str(item.get("State", "unknown"))
            containers.append(ContainerInfo(
                id=str(item["ID"]), name=str(item["Names"]), image=str(item["Image"]),
                state=state, status=str(item.get("Status", state)), running=state.lower() == "running",
            ))
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeCommandError("Docker returned an invalid container listing.") from exc
    return containers
