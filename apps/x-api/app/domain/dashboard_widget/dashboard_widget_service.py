from .dashboard_widget_repo import DashboardWidgetRepository
from .dashboard_widget_dto import DashboardWidgetCreateForm
from .dashboard_widget_entity import DashboardWidget

class DashboardWidgetService:
    """Service layer for DashboardWidget operations"""

    def __init__(self):
        self.repo = DashboardWidgetRepository()

    async def create(self) -> None:
        return await self.repo.create()

    async def find_all(self) -> list[DashboardWidget]:
        return await self.repo.find_all()

    async def find_one(self, uid: str) -> DashboardWidget:
        return await self.repo.find_one(uid)

    async def update(self, uid: str, form: DashboardWidgetCreateForm) -> DashboardWidget:
        return await self.repo.update(uid, form)

    async def remove(self, uid: str) -> None:
        return await self.repo.remove(uid)

    async def remove_all(self) -> None:
        return await self.repo.remove_all()