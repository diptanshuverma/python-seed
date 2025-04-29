"""
API Endpoints for Managing Publishers.
Defines endpoints for creating, retrieving, updating, and deleting publishers.
"""

from collections.abc import Sequence
from http import HTTPStatus

from fastapi import APIRouter

from app.db import AsyncSessionDep

from .publisher_dto import PublisherCreateForm, PublisherResult
from .publisher_entity import Publisher
from .publisher_service import PublisherService


# Router for publisher-related endpoints
publisher_router = APIRouter(
    prefix="/publisher",
    tags=["Publishers"]  # Tag for OpenAPI documentation
)

@publisher_router.post(
    "",
    response_model=PublisherResult,
    status_code=HTTPStatus.CREATED,
    summary="Create a New Publisher",
    description="Create a new publisher with the given details.",
)
async def create(form: PublisherCreateForm, session: AsyncSessionDep) -> Publisher:
    """
    Create a new publisher.

    Args:
        form (PublisherCreateForm): The details of the publisher to be created.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        PublisherResult: The created publisher's details.

    """
    service = PublisherService(session)
    return await service.create(form)

@publisher_router.post(
    "/create_many",
    response_model=list[PublisherResult],
    status_code=HTTPStatus.CREATED,
    summary="Load Publishers from a Parquet file.",
    description="Load new publishers from a Parquet file.",
)
async def create_many(forms: Sequence[PublisherCreateForm], session: AsyncSessionDep) -> list[Publisher]:
    """
    Create a new publisher.

    Args:
        form (PublisherCreateForm): The details of the publisher to be created.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        PublisherResult: The created publisher's details.

    """
    service = PublisherService(session)
    return await service.create_many(forms)

@publisher_router.post(
    "/create_from_parquet",
    response_model=list[PublisherResult],
    status_code=HTTPStatus.CREATED,
    summary="Load Publishers from a Parquet file.",
    description="Load new publishers from a Parquet file.",
)
async def create_from_parquet(parquet_path: str, session: AsyncSessionDep) -> list[Publisher]:
    """
    Create a new publisher.

    Args:
        form (PublisherCreateForm): The details of the publisher to be created.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        PublisherResult: The created publisher's details.

    """
    print("*******1")
    service = PublisherService(session)
    return await service.create_from_parquet(parquet_path)

@publisher_router.get(
    "",
    response_model=list[PublisherResult],
    status_code=HTTPStatus.OK,
    summary="Get All Publishers",
    description="Retrieve a list of all publishers.",
)
async def find_all(session: AsyncSessionDep) -> Sequence[Publisher]:
    """
    Retrieve all publishers.

    Args:
        session (AsyncSessionDep): The database session dependency.

    Returns:
        list[PublisherResult]: A list of all publishers.

    """
    service = PublisherService(session)
    return await service.find_all()

@publisher_router.get(
    "/{uid}",
    response_model=PublisherResult,
    status_code=HTTPStatus.OK,
    summary="Get Publisher by ID",
    description="Retrieve a publisher by its unique identifier (UID).",
)
async def find_one(uid: str, session: AsyncSessionDep) -> Publisher:
    """
    Retrieve a publisher by its unique identifier.

    Args:
        uid (str): The unique identifier of the publisher.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        PublisherResult: The requested publisher's details.

    """
    service = PublisherService(session)
    return await service.find_one(uid)

@publisher_router.put(
    "/{uid}",
    response_model=PublisherResult,
    status_code=HTTPStatus.OK,
    summary="Update a Publisher",
    description="Update the details of a publisher by its unique identifier (UID).",
)
async def update(uid: str, form: PublisherCreateForm, session: AsyncSessionDep) -> Publisher:
    """
    Update a publisher's details.

    Args:
        uid (str): The unique identifier of the publisher.
        form (PublisherCreateForm): The updated details of the publisher.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        PublisherResult: The updated publisher's details.

    """
    service = PublisherService(session)
    return await service.update(uid, form)

@publisher_router.delete(
    "/{uid}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete a Publisher",
    description="Delete a publisher by its unique identifier (UID).",
)
async def remove(uid: str, session: AsyncSessionDep) -> None:
    """
    Delete a publisher by its unique identifier.

    Args:
        uid (str): The unique identifier of the publisher.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        dict: An empty dictionary indicating success.

    """
    service = PublisherService(session)
    await service.remove(uid)
