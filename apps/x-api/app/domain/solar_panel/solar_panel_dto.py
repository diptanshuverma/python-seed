from datetime import datetime
from pydantic import BaseModel
from .solar_panel_entity import SolarPanel

class SolarPanelResult(SolarPanel):
    """Response model for SolarPanel data"""
    pass

class SolarPanelCreateForm(BaseModel):
    """Model for creating or updating SolarPanel records"""
    id: int
    voltage: float
    temperature: float
    status: str
    installation_timestamp: datetime
    latitude: float
    longitude: float