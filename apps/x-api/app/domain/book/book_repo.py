from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from common_fastapi import ResourceNotFoundException

from .book_dto import BookCreateForm
from .book_entity import Book


class BookRepository:
    """Repository layer for book operations."""

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session."""
        self.session = session

    async def create(self, form: BookCreateForm) -> Book:
        """Create a new book."""
        new_item = Book(**form.model_dump())
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item

    async def find_all(self) -> Sequence[Book]:
        """Retrieve all books."""
        statement = select(Book).order_by(Book.created_at)
        result = await self.session.execute(statement)
        return result.all()

    async def find_one(self, uid: str) -> Book:
        """Retrieve a book by ID."""
        statement = select(Book).where(Book.uid == uid)
        result = await self.session.execute(statement)
        item = result.first()
        if not item:
            raise ResourceNotFoundException(resource_name="Book")
        return item

    async def update(self, uid: str, form: BookCreateForm) -> Book:
        """Update a book by ID."""
        item = await self.find_one(uid)
        for key, value in form.model_dump().items():
            setattr(item, key, value)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def remove(self, uid: str) -> None:
        """Remove a book by ID."""
        item = await self.find_one(uid)
        await self.session.delete(item)
        await self.session.commit()
