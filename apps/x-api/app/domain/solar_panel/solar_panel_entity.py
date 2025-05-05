from datetime import datetime
from pydantic import BaseModel

class SolarPanelInformation(BaseModel):
    id: int
    voltage: float
    temperature: float
    status: str
    installation_timestamp: datetime

class SolarPanelLocation(BaseModel):
    id: int
    latitude: float
    longitude: float

class SolarPanel(BaseModel):
    id: int
    voltage: float
    temperature: float
    status: str
    installation_timestamp: datetime
    latitude: float
    longitude: float