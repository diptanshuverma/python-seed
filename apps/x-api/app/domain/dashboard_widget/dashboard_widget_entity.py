from datetime import datetime
from pydantic import BaseModel

class DashboardWidget(BaseModel):
    id: str
    name: str
    capacity: float  # in kW
    rotor_diameter: float  # in meters
    hub_height: float  # in meters
    manufacturer: str
    country: str
    installation_date: datetime
    status: str  # e.g. 'Active', 'Maintenance', 'Decommissioned'