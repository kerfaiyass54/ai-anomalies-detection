from pydantic import BaseModel, ConfigDict

from .visualization import KibanaVisualization


class KibanaVisualizationPage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    per_page: int
    total: int
    visualizations: list[KibanaVisualization]
