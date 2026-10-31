from pydantic import BaseModel, ConfigDict


class PodInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    namespace: str
    phase: str
    pod_ip: str | None = None
    node_name: str | None = None
    containers: list[str]
