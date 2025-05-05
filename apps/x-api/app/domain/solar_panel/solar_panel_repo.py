# import os
# import duckdb
# import pandas as pd
# from common_fastapi import ResourceNotFoundException
# from .solar_panel_dto import SolarPanelCreateForm
# from .solar_panel_entity import SolarPanel

# class SolarPanelRepository:
#     """Repository for managing solar panel data via DuckDB and Parquet files."""

#     INFO_PATH = "solar_panel_information.parquet"
#     LOCATION_PATH = "solar_panel_location.parquet"
#     JOINED_PATH = "solar_panel.parquet"

#     def __init__(self):
#         self.conn = duckdb.connect()

#     def create(self) -> None:
#         """Create joined solar panel data from information and location parquet files."""
#         # Join via DuckDB and write to parquet
#         self.conn.execute(f"""
#             CREATE OR REPLACE TABLE joined AS
#             SELECT info.id,
#                    info.voltage,
#                    info.temperature,
#                    info.status,
#                    info.installation_timestamp,
#                    loc.latitude,
#                    loc.longitude
#             FROM read_parquet('{self.INFO_PATH}') AS info
#             JOIN read_parquet('{self.LOCATION_PATH}') AS loc
#             USING (id)
#         """)
#         self.conn.execute(f"COPY joined TO '{self.JOINED_PATH}' (FORMAT PARQUET)")

#     def find_all(self) -> list[SolarPanel]:
#         """Retrieve all solar panel records from the joined parquet file."""
#         df = self.conn.execute(f"SELECT * FROM read_parquet('{self.JOINED_PATH}')").df()
#         return [SolarPanel(**row) for row in df.to_dict(orient='records')]

#     def find_one(self, uid: int) -> SolarPanel:
#         """Retrieve a single solar panel record by ID."""
#         df = self.conn.execute(
#             f"SELECT * FROM read_parquet('{self.JOINED_PATH}') WHERE id = {uid}"
#         ).df()
#         if df.empty:
#             raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
#         return SolarPanel(**df.iloc[0].to_dict())

#     def update(self, uid: int, form: SolarPanelCreateForm) -> SolarPanel:
#         """Update a solar panel record by ID."""
#         df = self.conn.execute(f"SELECT * FROM read_parquet('{self.JOINED_PATH}')").df()
#         if uid not in df['id'].values:
#             raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
#         for field, value in form.model_dump().items():
#             if field != 'id':
#                 df.loc[df['id'] == uid, field] = value
#         df.to_parquet(self.JOINED_PATH, index=False)
#         updated = df[df['id'] == uid].iloc[0].to_dict()
#         return SolarPanel(**updated)

#     def remove(self, uid: int) -> None:
#         """Delete a specific solar panel record by ID."""
#         df = self.conn.execute(f"SELECT * FROM read_parquet('{self.JOINED_PATH}')").df()
#         if uid not in df['id'].values:
#             raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
#         df = df[df['id'] != uid]
#         df.to_parquet(self.JOINED_PATH, index=False)

#     def remove_all(self) -> None:
#         """Delete the entire joined parquet file."""
#         if os.path.exists(self.JOINED_PATH):
#             os.remove(self.JOINED_PATH)

import duckdb
import pandas as pd
from pathlib import Path
from common_fastapi import ResourceNotFoundException
from .solar_panel_dto import SolarPanelCreateForm
from .solar_panel_entity import SolarPanel

class SolarPanelRepository:
    """Repository for managing solar panel data via DuckDB and Parquet files."""

    BASE_DIR = Path(__file__).parent
    INFO_PATH = BASE_DIR / "solar_panel_information.parquet"
    LOCATION_PATH = BASE_DIR / "solar_panel_location.parquet"
    JOINED_PATH = BASE_DIR / "solar_panel.parquet"

    def __init__(self):
        self.conn = duckdb.connect()

    def create(self) -> None:
        """Create joined solar panel data from information and location parquet files."""
        info_path = str(self.INFO_PATH)
        loc_path = str(self.LOCATION_PATH)
        joined_path = str(self.JOINED_PATH)
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE joined AS
            SELECT info.id,
                   info.voltage,
                   info.temperature,
                   info.status,
                   info.installation_timestamp,
                   loc.latitude,
                   loc.longitude
            FROM read_parquet('{info_path}') AS info
            JOIN read_parquet('{loc_path}') AS loc
            USING (id)
        """)
        self.conn.execute(f"COPY joined TO '{joined_path}' (FORMAT PARQUET)")

    def find_all(self) -> list[SolarPanel]:
        """Retrieve all solar panel records from the joined parquet file."""
        joined_path = str(self.JOINED_PATH)
        df = self.conn.execute(f"SELECT * FROM read_parquet('{joined_path}')").df()
        return [SolarPanel(**row) for row in df.to_dict(orient='records')]

    def find_one(self, uid: int) -> SolarPanel:
        """Retrieve a single solar panel record by ID."""
        joined_path = str(self.JOINED_PATH)
        df = self.conn.execute(
            f"SELECT * FROM read_parquet('{joined_path}') WHERE id = {uid}"
        ).df()
        if df.empty:
            raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
        return SolarPanel(**df.iloc[0].to_dict())

    def update(self, uid: int, form: SolarPanelCreateForm) -> SolarPanel:
        """Update a solar panel record by ID."""
        joined_path = str(self.JOINED_PATH)
        df = self.conn.execute(f"SELECT * FROM read_parquet('{joined_path}')").df()
        if uid not in df['id'].values:
            raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
        for field, value in form.model_dump().items():
            if field != 'id':
                df.loc[df['id'] == uid, field] = value
        df.to_parquet(joined_path, index=False)
        updated = df[df['id'] == uid].iloc[0].to_dict()
        return SolarPanel(**updated)

    def remove(self, uid: int) -> None:
        """Delete a specific solar panel record by ID."""
        joined_path = str(self.JOINED_PATH)
        df = self.conn.execute(f"SELECT * FROM read_parquet('{joined_path}')").df()
        if uid not in df['id'].values:
            raise ResourceNotFoundException(f"SolarPanel with id {uid} not found")
        df = df[df['id'] != uid]
        df.to_parquet(joined_path, index=False)

    def remove_all(self) -> None:
        """Delete the entire joined parquet file."""
        joined_path = self.JOINED_PATH
        if joined_path.exists():
            joined_path.unlink()