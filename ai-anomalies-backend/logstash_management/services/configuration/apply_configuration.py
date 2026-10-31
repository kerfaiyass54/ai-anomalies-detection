import time

from ...errors import ConfigurationServiceError
from ...schemas.configuration import ConfigurationResponse, ConfigurationSettings
from .configuration_files import read_generated_configuration, read_settings, write_settings
from .default_configuration import DEFAULT_SETTINGS, render_configuration
from .logstash_reload_status import get_reload_counts

RELOAD_TIMEOUT_SECONDS = 12


def _wait_for_reload(previous: tuple[int, int]) -> str:
    deadline = time.monotonic() + RELOAD_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        time.sleep(0.5)
        current = get_reload_counts()
        if current[1] > previous[1]:
            return "failed"
        if current[0] > previous[0]:
            return "applied"
    return "timeout"


def apply_configuration(settings: ConfigurationSettings | None) -> ConfigurationResponse:
    requested = settings or DEFAULT_SETTINGS
    previous, _ = read_settings()
    generated = render_configuration(requested)
    previous_generated = read_generated_configuration()
    if requested == previous and generated == previous_generated:
        return ConfigurationResponse(
            settings=requested,
            generated_configuration=generated,
            using_default=requested == DEFAULT_SETTINGS,
            reload_applied=True,
        )
    if generated == previous_generated:
        write_settings(requested, generated)
        return ConfigurationResponse(
            settings=requested,
            generated_configuration=generated,
            using_default=requested == DEFAULT_SETTINGS,
            reload_applied=True,
        )

    previous_counts = get_reload_counts()
    write_settings(requested, generated)
    reload_result = _wait_for_reload(previous_counts)
    if reload_result != "applied":
        write_settings(previous, previous_generated)
        if reload_result == "failed":
            try:
                _wait_for_reload(get_reload_counts())
            except ConfigurationServiceError:
                pass
            raise ConfigurationServiceError(
                "Logstash could not apply these settings; the previous settings were restored.",
                status_code=422,
            )
        raise ConfigurationServiceError(
            "Logstash did not confirm a reload; the previous settings were restored.", status_code=504
        )

    return ConfigurationResponse(
        settings=requested,
        generated_configuration=generated,
        using_default=requested == DEFAULT_SETTINGS,
        reload_applied=True,
    )
