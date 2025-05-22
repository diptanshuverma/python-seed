import json
from pathlib import Path
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from common_fastapi import ResourceNotFoundException
from .dashboard_widget_entity import DashboardWidget
from .dashboard_widget_dto import DashboardWidgetCreateForm

class DashboardWidgetRepository:
    """Async repository for DashboardWidget against MongoDB"""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    JSON_PATH = BASE_DIR / "windmill.json"

    def __init__(self, mongo_uri: str = None):
        uri = mongo_uri or "mongodb://localhost:27017"
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client["Widget"]
        self.collection = self.db["DashboardWidget"]

    async def create(self) -> None:
        # ensure collection exists
        names = await self.db.list_collection_names()
        if "DashboardWidget" not in names:
            await self.db.create_collection("DashboardWidget")
        # load data
        raw = json.loads(self.JSON_PATH.read_text())
        documents = []
        for doc in raw:
            # parse installation_date if present
            if 'installation_date' in doc:
                doc['installation_date'] = datetime.fromisoformat(doc['installation_date'])
            documents.append(doc)
        # insert many, ignoring duplicates on id
        await self.collection.insert_many(documents)

    async def find_all(self) -> list[DashboardWidget]:
        cursor = self.collection.find({})
        out = []
        async for doc in cursor:
            doc.pop('_id', None)
            out.append(DashboardWidget(**doc))
        return out

    async def find_one(self, uid: str) -> DashboardWidget:
        doc = await self.collection.find_one({"id": uid})
        if not doc:
            raise ResourceNotFoundException(f"DashboardWidget with id {uid} not found")
        doc.pop('_id', None)
        return DashboardWidget(**doc)

    async def update(self, uid: str, form: DashboardWidgetCreateForm) -> DashboardWidget:
        data = form.model_dump()
        result = await self.collection.update_one({"id": uid}, {"$set": data})
        if result.matched_count == 0:
            raise ResourceNotFoundException(f"DashboardWidget with id {uid} not found")
        return await self.find_one(uid)

    async def remove(self, uid: str) -> None:
        result = await self.collection.delete_one({"id": uid})
        if result.deleted_count == 0:
            raise ResourceNotFoundException(f"DashboardWidget with id {uid} not found")

    async def remove_all(self) -> None:
        await self.collection.delete_many({})