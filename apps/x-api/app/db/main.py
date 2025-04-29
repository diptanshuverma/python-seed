"""
This module handles database setup and management using SQLModel with SQLAlchemy's async engine.
It includes functions for initializing the database and providing an asynchronous session
for interacting with the database.

Modules:
- app.config: Provides the application settings, including database configuration.
- sqlalchemy.ext.asyncio: Provides support for asynchronous database operations.
- sqlmodel: A library for working with SQL databases using Python objects.
"""

from collections.abc import AsyncGenerator
from typing import Annotated, cast

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import app_settings
from common_fastapi import APP_ENV, AppEnv, DbConnectionException


# Create the async engine for database connection
async_engine = create_async_engine(
    url=cast(str, app_settings.DATABASE_URL),  # Database URL from application settings
    echo=True,  # Enable SQLAlchemy query logging for debugging purposes
    poolclass=NullPool if APP_ENV == AppEnv.TESTING else AsyncAdaptedQueuePool,  # pytest-asyncio works with NullPool
    pool_pre_ping=True,
)

async def init_db() -> None:
    """
    Initialize the database by creating all the tables defined in the SQLModel metadata.

    This function is typically called during application startup to ensure that
    all required database tables exist. It uses the async engine to interact
    with the database.

    TODO: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters

    Raises
    ------
    SQLAlchemyError: If there's an error during table creation.

    """
    async with async_engine.begin() as conn:
        # Use `run_sync` to synchronize the creation of all tables
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to provide an asynchronous session for database interactions.
    This function generates an AsyncSession instance bound to the async engine
    and ensures proper cleanup by closing the session after use.

    Yields
    ------
    AsyncSession: An active session for executing database operations.

    """
    # Create a session factory with the async engine
    async_session_factory = sessionmaker(
        bind=async_engine,           # Bind the session to the async engine
        class_=AsyncSession,         # Use the async session class
        expire_on_commit=False,      # Prevent automatic expiration of instances after commit
    )

    # Provide the session to the caller and clean up after use
    try:
        async with async_session_factory() as session:
            yield session
    except OSError as db_exc:
        # Handle database connection errors gracefully
        raise DbConnectionException() from db_exc

# Type alias for dependency injection of an AsyncSession
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
"""
This alias simplifies the usage of the get_session dependency in FastAPI endpoints.
By annotating a parameter with `AsyncSessionDep`, the endpoint will receive an
`AsyncSession` instance automatically.

Example:
    @app.get("/example")
    async def example_endpoint(session: AsyncSessionDep):
        # Use `session` to interact with the database
"""
