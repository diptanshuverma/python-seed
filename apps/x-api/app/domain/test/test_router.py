import logging

from fastapi import APIRouter


logger = logging.getLogger(__name__)

test_router = APIRouter(prefix="/test")

@test_router.get("", response_model=dict[str, str])
async def read_root() -> dict[str, str]:
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    return {"Hello": "World"}
