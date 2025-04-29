from pydantic import BaseModel, Field


# Pydantic models for the response

class HealthIndicator(BaseModel):
    status: str = Field(..., description="The status of the health indicator ('up' or 'down').")
    message: str | None = Field(None, description="Optional error message for unhealthy indicators.")
    latency: int | None = Field(None, description="Latency in milliseconds, if applicable.")


class HealthCheckResult(BaseModel):
    status: str = Field(..., description="Overall health status: 'OK', 'error'")
    info: dict[str, HealthIndicator] = Field(..., description="Info of healthy indicators.")
    error: dict[str, HealthIndicator] = Field(..., description="Info of unhealthy indicators.")
    details: dict[str, HealthIndicator] = Field(..., description="Detailed info of all indicators.")
