import json
import os
import tempfile
from pathlib import Path

from ...errors import ConfigurationServiceError
from ...schemas.configuration import ConfigurationSettings
from .default_configuration import DEFAULT_SETTINGS, render_configuration


def get_config_directory() -> Path:
    return Path(os.getenv("LOGSTASH_CONFIG_DIRECTORY", "/pipeline"))


def _atomic_write(path: Path, content: str) -> None:
    temporary_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=".pipeline-", suffix=".tmp", delete=False
        ) as temporary_file:
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, path)
    except OSError as exc:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise ConfigurationServiceError("Could not persist the Logstash settings.") from exc


def read_settings() -> tuple[ConfigurationSettings, bool]:
    path = get_config_directory() / "user-settings.json"
    try:
        settings = ConfigurationSettings.model_validate_json(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return DEFAULT_SETTINGS, True
    except (OSError, ValueError) as exc:
        raise ConfigurationServiceError("Stored Logstash settings could not be read.") from exc
    return settings, settings == DEFAULT_SETTINGS


def read_generated_configuration() -> str:
    path = get_config_directory() / "logstash.conf"
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return render_configuration(DEFAULT_SETTINGS)
    except OSError as exc:
        raise ConfigurationServiceError("The active Logstash pipeline could not be read.") from exc


def write_settings(settings: ConfigurationSettings, generated_configuration: str) -> None:
    directory = get_config_directory()
    _atomic_write(directory / "user-settings.json", settings.model_dump_json(indent=2))
    _atomic_write(directory / "logstash.conf", generated_configuration)
