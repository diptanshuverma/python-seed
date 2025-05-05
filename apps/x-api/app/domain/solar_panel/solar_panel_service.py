from .solar_panel_dto import SolarPanelCreateForm
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

    def find_one(self, uid: int) -> SolarPanel:
        return self.repo.find_one(uid)

    def update(self, uid: int, form: SolarPanelCreateForm) -> SolarPanel:
        return self.repo.update(uid, form)

    def remove(self, uid: int) -> None:
        return self.repo.remove(uid)

    def remove_all(self) -> None:
        return self.repo.remove_all()