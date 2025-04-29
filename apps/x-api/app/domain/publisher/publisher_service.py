from collections.abc import Sequence

from sqlmodel.ext.asyncio.session import AsyncSession

from .publisher_dto import PublisherCreateForm
from .publisher_entity import Publisher
from .publisher_repo import PublisherRepository


class PublisherService:
    """Service layer for managing publishers."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the service with a database session."""
        self.repo = PublisherRepository(session)

    async def create(self, form: PublisherCreateForm) -> Publisher:
        """Create a new publisher."""
        return await self.repo.create(form)
    
    async def create_many(self, forms: Sequence[PublisherCreateForm]) -> list[Publisher]:
        """Create a new publisher."""
        return await self.repo.create_many(forms)
    
    async def create_from_parquet(self, parquet_path: str) -> list[Publisher]:
        """Create a new publisher."""
        print("******2")
        return await self.repo.create_from_parquet(parquet_path)

    async def find_all(self) -> Sequence[Publisher]:
        """Retrieve all publishers."""
        return await self.repo.find_all()

    async def find_one(self, uid: str) -> Publisher:
        """Retrieve a publisher by ID."""
        return await self.repo.find_one(uid)

    async def update(self, uid: str, form: PublisherCreateForm) -> Publisher:
        """Update a publisher by ID."""
        return await self.repo.update(uid, form)

    async def remove(self, uid: str) -> None:
        """Remove a publisher by ID."""
        await self.repo.remove(uid)
