from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConfigurationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_path: str = "/var/log/containers/*.log"
    start_position: Literal["beginning", "end"] = "beginning"
    elasticsearch_index: str = "logs"

    @field_validator("input_path")
    @classmethod
    def validate_input_path(cls, value: str) -> str:
        if (
            not value.startswith("/var/log/containers/")
            or ".." in value.split("/")
            or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./*-?" for character in value)
        ):
            raise ValueError("input_path must be a file pattern under /var/log/containers.")
        return value

    @field_validator("elasticsearch_index")
    @classmethod
    def validate_index(cls, value: str) -> str:
        if not value or len(value) > 200 or not all(
            character in "abcdefghijklmnopqrstuvwxyz0123456789._-" for character in value
        ) or value[0] in "._-":
            raise ValueError("elasticsearch_index must be a valid lowercase Elasticsearch index name.")
        return value


class ConfigurationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    settings: ConfigurationSettings | None = Field(default=None)


class ConfigurationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    settings: ConfigurationSettings
    generated_configuration: str
    using_default: bool
    reload_applied: bool
