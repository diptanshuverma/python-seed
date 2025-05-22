from pydantic import BaseModel
from .dashboard_widget_entity import DashboardWidget
from datetime import datetime

class DashboardWidgetResult(DashboardWidget):
    """Response DTO for DashboardWidget"""
    pass

class DashboardWidgetCreateForm(BaseModel):
    """Request DTO for creating/updating DashboardWidget"""
    id: str
    name: str
    capacity: float
    rotor_diameter: float
    hub_height: float
    manufacturer: str
    country: str
    installation_date: datetime
    status: str