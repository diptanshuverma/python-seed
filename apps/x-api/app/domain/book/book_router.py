"""
API Endpoints for Managing Books.
Defines endpoints for creating, retrieving, updating, and deleting books.
"""

from collections.abc import Sequence
from http import HTTPStatus

from fastapi import APIRouter

from app.db import AsyncSessionDep

from .book_dto import BookCreateForm, BookResult
from .book_entity import Book
from .book_service import BookService


# Router for book-related endpoints
book_router = APIRouter(
    prefix="/book",
    tags=["Books"]  # Tag for OpenAPI documentation
)

@book_router.post(
    "",
    response_model=BookResult,
    status_code=HTTPStatus.CREATED,
    summary="Create a New Book",
    description="Create a new book with the given details.",
)
async def create(form: BookCreateForm, session: AsyncSessionDep) -> Book:
    """
    Create a new book.

    Args:
        form (BookCreateForm): The details of the book to be created.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        BookResult: The created book's details.

    """
    service = BookService(session)
    return await service.create(form)

@book_router.get(
    "",
    response_model=list[BookResult],
    status_code=HTTPStatus.OK,
    summary="Get All Books",
    description="Retrieve a list of all books.",
)
async def find_all(session: AsyncSessionDep) -> Sequence[Book]:
    """
    Retrieve all books.

    Args:
        session (AsyncSessionDep): The database session dependency.

    Returns:
        list[BookResult]: A list of all books.

    """
    service = BookService(session)
    return await service.find_all()

@book_router.get(
    "/{uid}",
    response_model=BookResult,
    status_code=HTTPStatus.OK,
    summary="Get Book by ID",
    description="Retrieve a book by its unique identifier (UID).",
)
async def find_one(uid: str, session: AsyncSessionDep) -> Book:
    """
    Retrieve a book by its unique identifier.

    Args:
        uid (str): The unique identifier of the book.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        BookResult: The requested book's details.

    """
    service = BookService(session)
    return await service.find_one(uid)

@book_router.put(
    "/{uid}",
    response_model=BookResult,
    status_code=HTTPStatus.OK,
    summary="Update a Book",
    description="Update the details of a book by its unique identifier (UID).",
)
async def update(uid: str, form: BookCreateForm, session: AsyncSessionDep) -> Book:
    """
    Update a book's details.

    Args:
        uid (str): The unique identifier of the book.
        form (BookCreateForm): The updated details of the book.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        BookResult: The updated book's details.

    """
    service = BookService(session)
    return await service.update(uid, form)

@book_router.delete(
    "/{uid}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete a Book",
    description="Delete a book by its unique identifier (UID).",
)
async def remove(uid: str, session: AsyncSessionDep) -> None:
    """
    Delete a book by its unique identifier.

    Args:
        uid (str): The unique identifier of the book.
        session (AsyncSessionDep): The database session dependency.

    Returns:
        dict: An empty dictionary indicating success.

    """
    service = BookService(session)
    await service.remove(uid)
