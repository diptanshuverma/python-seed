import logging
from typing import Any

from pydantic import PostgresDsn, field_validator

from common_fastapi import EnvSettings


logger = logging.getLogger(__name__)

class AppSettings(EnvSettings):
    """
    Comprehensive application settings class that includes both database configurations
    and other application-specific settings.

    Attributes:
        POSTGRES_USER (str): PostgreSQL username.
        POSTGRES_PASSWORD (str): PostgreSQL password.
        POSTGRES_DB (str): PostgreSQL database name.
        POSTGRES_HOST (str): PostgreSQL host.
        POSTGRES_PORT (int): PostgreSQL port.
        DATABASE_URL (str): Constructed PostgreSQL DSN as a string.

    """

    model_config = {
        "extra": "ignore",         # Ignore extra fields from the environment
        "populate_by_name": True  # Allow population by explicitly defined fields
    }

    # Database configuration
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    DATABASE_URL: str | None = None  # Make DATABASE_URL a string

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, _: Any, info: Any) -> str:  # pylint: disable=no-self-argument
        """
        Assemble the PostgreSQL DSN from individual components.

        Args:
            v (Optional[str]): Existing DATABASE_URL value.
            info (ValidationInfo): Contains model field values and validation context.

        Returns:
            str: Constructed database connection string.

        """
        data = info.data  # Access field values as a dictionary

        # Build the connection string as a string, not as PostgresDsn
        db_url = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=data["POSTGRES_USER"],
            password=data["POSTGRES_PASSWORD"],
            host=data["POSTGRES_HOST"],
            port=data["POSTGRES_PORT"],
            path=data["POSTGRES_DB"],
        )

        return str(db_url)  # Convert PostgresDsn to a string


# Instantiate the settings object to make configurations accessible globally
app_settings = AppSettings()
