from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
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
    
class PaginatedSolarPanel(BaseModel):
    """Pagination response schema for SolarPanel"""
    page_size: int
    current_page: int
    total_records: int
    next_page: Optional[int]
    previous_page: Optional[int]
    SolarPanel: List[SolarPanelResult]