from collections.abc import Sequence

from sqlmodel.ext.asyncio.session import AsyncSession

from .book_dto import BookCreateForm
from .book_entity import Book
from .book_repo import BookRepository


class BookService:
    """Service layer for managing books."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the service with a database session."""
        self.repo = BookRepository(session)

    async def create(self, form: BookCreateForm) -> Book:
        """Create a new book."""
        return await self.repo.create(form)

    async def find_all(self) -> Sequence[Book]:
        """Retrieve all books."""
        return await self.repo.find_all()

    async def find_one(self, uid: str) -> Book:
        """Retrieve a book by ID."""
        return await self.repo.find_one(uid)

    async def update(self, uid: str, form: BookCreateForm) -> Book:
        """Update a book by ID."""
        return await self.repo.update(uid, form)

    async def remove(self, uid: str) -> None:
        """Remove a book by ID."""
        await self.repo.remove(uid)
