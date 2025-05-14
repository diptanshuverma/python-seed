from pydantic import BaseModel

class InferenceInputEntity(BaseModel):
    """Domain entity for inference input features"""
    voltage: float
    temperature: float
    latitude: float
    longitude: float
    panel_age_days: int

class InferenceResultEntity(BaseModel):
    """Domain entity for inference output"""
    predicted_status: str
    probabilities: dict[str, float]