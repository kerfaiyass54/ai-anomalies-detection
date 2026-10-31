import json

from ..errors import RuntimeCommandError
from ..schemas import PodInfo
from .command import run_command


def list_pods(*, namespace: str | None = None) -> list[PodInfo]:
    """List pods in all namespaces, or in one requested namespace."""
    command = ["kubectl", "get", "pods"]
    command.extend(["--namespace", namespace] if namespace else ["--all-namespaces"])
    command.extend(["--output", "json"])
    output = run_command(command)
    try:
        payload = json.loads(output)
        return [
            PodInfo(
                name=item["metadata"]["name"],
                namespace=item["metadata"].get("namespace", "default"),
                phase=item.get("status", {}).get("phase", "Unknown"),
                pod_ip=item.get("status", {}).get("podIP"),
                node_name=item.get("spec", {}).get("nodeName"),
                containers=[container["name"] for container in item.get("spec", {}).get("containers", []) if "name" in container],
            )
            for item in payload.get("items", [])
        ]
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeCommandError("kubectl returned an invalid pod listing.") from exc
