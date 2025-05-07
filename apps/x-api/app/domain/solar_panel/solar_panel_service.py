from .solar_panel_dto import SolarPanelCreateForm, PaginatedSolarPanel, SolarPanelResult
from .solar_panel_entity import SolarPanel
from .solar_panel_repo import SolarPanelRepository

class SolarPanelService:
    """Service layer for managing solar panel operations."""

    def __init__(self) -> None:
        self.repo = SolarPanelRepository()

    def create(self) -> None:
        return self.repo.create()

    def find_all(self) -> list[SolarPanel]:
        return self.repo.find_all()

    def find_all_by_pagination(self, limit: int, page_number: int) -> PaginatedSolarPanel:
        entities, total = self.repo.find_all_by_pagination(limit, page_number)
        items = [SolarPanelResult(**e.model_dump()) for e in entities]
        next_page = page_number + 1 if page_number * limit < total else None
        previous_page = page_number - 1 if page_number > 1 else None
        return PaginatedSolarPanel(
            page_size=limit,
            current_page=page_number,
            total_records=total,
            next_page=next_page,
            previous_page=previous_page,
            SolarPanel=items
        )

    def find_one(self, uid: int) -> SolarPanel:
        return self.repo.find_one(uid)

    def update(self, uid: int, form: SolarPanelCreateForm) -> SolarPanel:
        return self.repo.update(uid, form)

    def remove(self, uid: int) -> None:
        return self.repo.remove(uid)

    def remove_all(self) -> None:
        return self.repo.remove_all()