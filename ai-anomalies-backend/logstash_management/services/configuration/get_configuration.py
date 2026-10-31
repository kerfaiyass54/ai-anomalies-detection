from ...schemas.configuration import ConfigurationResponse
from .configuration_files import read_generated_configuration, read_settings


def get_configuration() -> ConfigurationResponse:
    settings, using_default = read_settings()
    generated = read_generated_configuration()
    return ConfigurationResponse(
        settings=settings,
        generated_configuration=generated,
        using_default=using_default,
        reload_applied=True,
    )
