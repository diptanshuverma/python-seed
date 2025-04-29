"""
This module initializes and configures the FastAPI application for the `x_api` service.
It defines the application's lifespan events, includes the necessary routes,
and sets up the database initialization.

Modules:
- common_fastapi: Provides the reusable `create_app` function to create a FastAPI app with custom configurations.
- db.main: Contains the logic to initialize the database.
- domain.books.routes: Defines the API routes related to books.
- domain.test.routes: Defines the API routes for testing purposes.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from common_fastapi import create_app

# Import database initialization function
from .db import init_db

# Import routers for API endpoints
from .domain import book_router, health_router, test_router, publisher_router


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    Define the application's lifespan context manager.
    This is used to perform setup and teardown tasks during the app's lifecycle.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance that the lifespan context manager is associated with.
        It allows access to the app instance during setup and teardown phases.

    Yields
    ------
    None
        Indicates the app has been successfully initialized and is ready to run.

    """
    try:
        # Attempt to initialize the database
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:  # pylint: disable=broad-except
        # Log the exception and allow the app to start
        logger.error("Failed to initialize the database: %s", e)

    # Continue running the app even if the database initialization fails
    yield
    # Perform any cleanup tasks here if needed in the future


# Create the FastAPI application instance with specific configurations
# The `lifespan` context manager handles setup and teardown logic.
app = create_app(
    app_name="x_api",  # The name of the application, used for identification
    lifespan=lifespan,  # Custom lifespan manager for initialization and cleanup
)

# Include the API routes into the application
app.include_router(book_router)
app.include_router(publisher_router)
app.include_router(test_router)
app.include_router(health_router)
