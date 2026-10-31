from fastapi import APIRouter, Depends, HTTPException

from ..errors import ConfigurationServiceError
from ..schemas import ConfigurationResponse, ConfigurationUpdate
from ..security import require_admin_token
from ..services.configuration import apply_configuration, get_configuration

router = APIRouter(
    prefix="/api/v1/logstash/config",
    tags=["Logstash configuration"],
    dependencies=[Depends(require_admin_token)],
)


@router.get("", response_model=ConfigurationResponse)
def read_configuration() -> ConfigurationResponse:
    try:
        return get_configuration()
    except ConfigurationServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.put("", response_model=ConfigurationResponse)
def update_configuration(request: ConfigurationUpdate) -> ConfigurationResponse:
    try:
        return apply_configuration(request.settings)
    except ConfigurationServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
