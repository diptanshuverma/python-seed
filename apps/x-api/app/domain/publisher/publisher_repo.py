from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from common_fastapi import ResourceNotFoundException

from .publisher_dto import PublisherCreateForm
from .publisher_entity import Publisher
import pyarrow.parquet as pq
from pyiceberg.catalog import load_catalog

class PublisherRepository:
    """Repository layer for publisher operations."""

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session."""
        self.session = session

    async def create(self, form: PublisherCreateForm) -> Publisher:
        """Create a new publisher."""
        new_item = Publisher(**form.model_dump())
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item
    
    async def create_many(self, forms: Sequence[PublisherCreateForm]) -> list[Publisher]:
        """Create multiple publishers."""
        new_items = [Publisher(**form.model_dump()) for form in forms]
        self.session.add_all(new_items)
        await self.session.commit()
        for item in new_items:
            await self.session.refresh(item)
        return new_items
    
    async def create_from_parquet(self, parquet_path: str) -> list[Publisher]:
        """Create publishers from a parquet file."""
        print("*******3")
        
        warehouse_path = "/tmp/warehouse"
        catalog = load_catalog(
            "default",
            **{
                "type": "sql",
                "uri": f"sqlite:///{warehouse_path}/pyiceberg_catalog.db",
                "warehouse": f"file://{warehouse_path}",
            },
        )
        
        df = pq.read_table("/tmp/dummy_publishers.parquet")
        
        # Step 1: Read parquet into PyArrow Table
        # table = pq.read_table(parquet_path)
        
        print("*****3.1 ")

        # Step 2: Convert to Pandas DataFrame
        df = df.to_pandas()
        
        print("df contents :- -:- -:- -:")
        #print(df)
        print("*******4")

        # Step 3: Convert to list of PublisherCreateForm objects
        forms = [
            PublisherCreateForm(**record)
            for record in df.to_dict(orient="records")
        ]

        # Step 4: Reuse existing create_many method
        return await self.create_many(forms)

    async def find_all(self) -> Sequence[Publisher]:
        """Retrieve all publishers."""
        statement = select(Publisher).order_by(Publisher.created_at)
        result = await self.session.execute(statement)
        return result.all()

    async def find_one(self, uid: str) -> Publisher:
        """Retrieve a publisher by ID."""
        statement = select(Publisher).where(Publisher.uid == uid)
        result = await self.session.execute(statement)
        item = result.first()
        if not item:
            raise ResourceNotFoundException(resource_name="Publisher")
        return item

    async def update(self, uid: str, form: PublisherCreateForm) -> Publisher:
        """Update a publisher by ID."""
        item = await self.find_one(uid)
        for key, value in form.model_dump().items():
            setattr(item, key, value)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def remove(self, uid: str) -> None:
        """Remove a publisher by ID."""
        item = await self.find_one(uid)
        await self.session.delete(item)
        await self.session.commit()
