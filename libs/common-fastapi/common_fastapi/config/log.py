
import logging
import socket
from typing import TYPE_CHECKING, Any, cast

import structlog

from .cli_env import APP_ENV
from .enums.app_env import AppEnv
from .pretty_console_renderer import PrettyConsoleRenderer
from .settings import app_settings


if TYPE_CHECKING:
    from structlog.types import Processor

# Retrieve the hostname once
HOSTNAME = socket.gethostname()

def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger with the given name."""
    return structlog.stdlib.get_logger(name)

def get_log_context() -> dict[str, Any]:
    """Retrieve the current log context data."""
    return structlog.contextvars.get_contextvars()

def add_to_log_context(key: str, value: Any) -> None:
    """Set a key-value pair in the log context."""
    structlog.contextvars.bind_contextvars(**{key: value})

def clear_log_context() -> None:
    """Clear the structlog context variables."""
    structlog.contextvars.clear_contextvars()

def configure_logging(app_name: str) -> None:
    # Read log level from AppSettings
    log_level = app_settings.LOG_LEVEL.upper()  # pylint: disable=no-member

    def add_global_log_fields(_: Any, __: Any, event_dict: dict[str, Any]) -> dict[str, Any]:
        event_dict["name"] = app_name
        event_dict["hostname"] = HOSTNAME
        return event_dict

    # Define common processors
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=APP_ENV == AppEnv.PRODUCTION),
        cast(structlog.types.Processor, add_global_log_fields),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PROCESS,
            }
        ),
    ]

    if APP_ENV == AppEnv.PRODUCTION:
        shared_processors.extend(
            [
                structlog.processors.dict_tracebacks,
                structlog.processors.format_exc_info,
            ]
        )

    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    log_renderer = (
        structlog.processors.JSONRenderer()
        if APP_ENV == AppEnv.PRODUCTION
        else PrettyConsoleRenderer()  # structlog.dev.ConsoleRenderer()
    )

    # Set up formatter and handler
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            cast(structlog.types.Processor, log_renderer),
        ],
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    for _log in ["uvicorn", "uvicorn.error", "sqlalchemy.engine.Engine"]:
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True

    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = False
