import duckdb
import pandas as pd
from pathlib import Path
from common_fastapi import ResourceNotFoundException
from .solar_panel_dto import SolarPanelCreateForm
from .solar_panel_entity import SolarPanel

class SolarPanelRepository:
    """Repository for managing solar panel data via DuckDB and Parquet files."""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "solar_panel_data"
    INFO_PATH = DATA_DIR / "solar_panel_information.parquet"
    LOCATION_PATH = DATA_DIR / "solar_panel_location.parquet"
    JOINED_PATH = DATA_DIR / "solar_panel.parquet"

    def __init__(self):
        self.conn = duckdb.connect()

    def create(self) -> None:
        """Create joined solar panel data from information and location parquet files."""
        info_file = str(self.INFO_PATH)
        loc_file = str(self.LOCATION_PATH)
        out_file = str(self.JOINED_PATH)
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE joined AS
            SELECT info.id,
                   info.voltage,
                   info.temperature,
                   info.status,
                   info.installation_timestamp,
                   loc.latitude,
                   loc.longitude
            FROM read_parquet('{info_file}') AS info
            JOIN read_parquet('{loc_file}') AS loc
            USING (id)
        """)
        self.conn.execute(f"COPY joined TO '{out_file}' (FORMAT PARQUET)")

    def find_all(self) -> list[SolarPanel]:
        """Retrieve all solar panel records from joined data."""
        info_file = str(self.INFO_PATH)
        loc_file = str(self.LOCATION_PATH)
        query = f"""
            SELECT info.id,
                   info.voltage,
                   info.temperature,
                   info.status,
                   info.installation_timestamp,
                   loc.latitude,
                   loc.longitude
            FROM read_parquet('{info_file}') AS info
            JOIN read_parquet('{loc_file}') AS loc
            USING (id)
        """
        df = self.conn.execute(query).df()
        return [SolarPanel(**row) for row in df.to_dict(orient='records')]

    def find_all_by_pagination(self, limit: int, page_number: int) -> list[SolarPanel]:
        """Retrieve paginated solar panel records."""
        offset = (page_number - 1) * limit
        info_file = str(self.INFO_PATH)
        loc_file = str(self.LOCATION_PATH)
        query = f"""
            SELECT info.id,
                   info.voltage,
                   info.temperature,
                   info.status,
                   info.installation_timestamp,
                   loc.latitude,
                   loc.longitude
            FROM read_parquet('{info_file}') AS info
            JOIN read_parquet('{loc_file}') AS loc
            USING (id)
            LIMIT {limit} OFFSET {offset}
        """
        df = self.conn.execute(query).df()
        return [SolarPanel(**row) for row in df.to_dict(orient='records')]

    def find_one(self, uid: int) -> SolarPanel:
        """Retrieve a single solar panel record by ID."""
        info_file = str(self.INFO_PATH)
        loc_file = str(self.LOCATION_PATH)
        query = f"""
            SELECT info.id,
                   info.voltage,
                   info.temperature,
                   info.status,
                   info.installation_timestamp,
                   loc.latitude,
                   loc.longitude
            FROM read_parquet('{info_file}') AS info
            JOIN read_parquet('{loc_file}') AS loc
            USING (id)
            WHERE id = {uid}
        """
        df = self.conn.execute(query).df()
        if df.empty:
            raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
        return SolarPanel(**df.iloc[0].to_dict())

    def update(self, uid: int, form: SolarPanelCreateForm) -> SolarPanel:
        """Update a solar panel record by ID in the joined parquet file."""
        jp = str(self.JOINED_PATH)
        df = self.conn.execute(f"SELECT * FROM read_parquet('{jp}')").df()
        if uid not in df['id'].values:
            raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
        for field, value in form.model_dump().items():
            if field != 'id':
                df.loc[df['id'] == uid, field] = value
        df.to_parquet(jp, index=False)
        return SolarPanel(**df[df['id'] == uid].iloc[0].to_dict())

    def remove(self, uid: int) -> None:
        """Delete a specific solar panel record by ID from the joined parquet file."""
        jp = str(self.JOINED_PATH)
        df = self.conn.execute(f"SELECT * FROM read_parquet('{jp}')").df()
        if uid not in df['id'].values:
            raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
        df = df[df['id'] != uid]
        df.to_parquet(jp, index=False)

    def remove_all(self) -> None:
        """Delete the entire joined parquet file."""
        if self.JOINED_PATH.exists():
            self.JOINED_PATH.unlink()