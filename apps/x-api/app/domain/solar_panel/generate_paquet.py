# generate_parquets.py

import pandas as pd
import numpy as np
from datetime import datetime

def generate_solar_panel_information(path: str, num_records: float = 1000):
    """Generate a Parquet file with columns:
       id, voltage, temperature, status, installation_timestamp"""
    info_data = {
        "id": list(range(1, num_records + 1)),
        "voltage": np.random.uniform(200.0, 350.0, size=num_records),
        "temperature": np.random.uniform(10.0, 50.0, size=num_records),
        "status": np.random.choice(["OK", "Maintenance", "Fault"], size=num_records),
        "installation_timestamp": pd.to_datetime(
            np.random.randint(
            datetime(2015, 1, 1).timestamp(),
            datetime(2025, 1, 1).timestamp(),
            size=num_records
            ),
            unit="s"
        ),
    }
    df = pd.DataFrame(info_data)
    df.to_parquet(path, engine="pyarrow", index=False)
    print(f"Written {num_records} rows to {path}")

def generate_solar_panel_location(path: str, num_records: int = 1000):
    """Generate a Parquet file with columns:
       id, latitude, longitude"""
    loc_data = {
        "id": list(range(1, num_records + 1)),
        "latitude": np.random.uniform(-90.0, 90.0, size=num_records),
        "longitude": np.random.uniform(-180.0, 180.0, size=num_records),
    }
    df = pd.DataFrame(loc_data)
    df.to_parquet(path, engine="pyarrow", index=False)
    print(f"Written {num_records} rows to {path}")

if __name__ == "__main__":
    # adjust paths or record counts as you like
    generate_solar_panel_information(
        path="solar_panel_information.parquet",
        num_records=100000
    )
    generate_solar_panel_location(
        path="solar_panel_location.parquet",
        num_records=100000
    )