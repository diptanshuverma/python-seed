import time
from http import HTTPStatus
from typing import cast
from urllib.parse import urlparse, urlunparse

import asyncpg
from fastapi import APIRouter

from app.config import app_settings

from .health_dto import HealthCheckResult, HealthIndicator


# Router for health-related endpoints
health_router = APIRouter(
    prefix="/health",
    tags=["Health"],  # Tag for OpenAPI documentation
)

@health_router.get(
    "",
    response_model=HealthCheckResult,
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK,
    summary="Get Book by ID",
    description="Retrieve a book by its unique identifier (UID).",
)
async def check() -> HealthCheckResult:
    db_status = await check_database(cast(str, app_settings.DATABASE_URL))

    # Determine overall status
    overall_status = "error" if db_status.status == "down" else "ok"

    # Serialize database status once
    serialized_db_status = db_status.model_dump()

    # Build response
    response = HealthCheckResult(
        status=overall_status,
        info={"database": serialized_db_status} if db_status.status == "up" else {},
        error={"database": serialized_db_status} if db_status.status == "down" else {},
        details={"database": serialized_db_status},
    )

    return response


# Database health checker using SQLModel
async def check_database(url: str) -> HealthIndicator:
    """
    Check the health of the database by attempting a connection.

    Parameters
    ----------
    url : str
        The database connection URL.

    Returns
    -------
    HealthIndicator
        The health status of the database.

    """
    try:
        # Parse and adapt the database URL
        parsed_url = urlparse(url)
        if parsed_url.scheme == "postgresql+asyncpg":
            modified_url = urlunparse(parsed_url._replace(scheme="postgresql"))
        else:
            modified_url = url

        start_time = time.time()
        conn = await asyncpg.connect(modified_url)
        await conn.close()
        latency = int((time.time() - start_time) * 1000)  # Convert to milliseconds
        return HealthIndicator(status="up", latency=latency)
    except Exception as e:  # pylint: disable=broad-except
        # Return database down status with the error message
        return HealthIndicator(status="down", message=str(e))
