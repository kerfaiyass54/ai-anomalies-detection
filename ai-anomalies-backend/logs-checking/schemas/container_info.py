from pydantic import BaseModel, ConfigDict


class ContainerInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    image: str
    state: str
    status: str
    running: bool
