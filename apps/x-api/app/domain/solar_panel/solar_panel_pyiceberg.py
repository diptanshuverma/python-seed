from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
from pyiceberg.catalog import load_catalog

# FastAPI instance
app = FastAPI()

# Iceberg REST catalog config
catalog = load_catalog(
    name="rest",
    uri="http://localhost:8181",
    warehouse="s3://warehouse",
    s3={
        "endpoint": "http://localhost:9000",
        "access-key": "admin",
        "secret-key": "password"
    }
)

# Data model for appending
class SolarDataRecord(BaseModel):
    id: int
    voltage: float
    temperature: float
    status: str
    installation_timestamp: int
    latitude: float
    longitude: float

@app.get("/read-all/")
def read_all():
    start = time.time()

    table = catalog.load_table("default.solar_data")
    rows = []
    for batch in table.scan().to_arrow():
        rows.extend(batch.to_pylist())

    end = time.time()
    return {
        "rows_read": len(rows),
        "data": rows,
        "time_seconds": round(end - start, 3)
    }

@app.get("/read-id/{record_id}")
def read_by_id(record_id: int):
    start = time.time()

    table = catalog.load_table("default.solar_data")
    filtered_rows = []

    for batch in table.scan().filter(f"id == {record_id}").to_arrow():
        filtered_rows.extend(batch.to_pylist())

    end = time.time()
    if not filtered_rows:
        raise HTTPException(status_code=404, detail="Record not found")

    return {
        "rows_read": len(filtered_rows),
        "data": filtered_rows,
        "time_seconds": round(end - start, 3)
    }

@app.post("/append/")
def append_record(record: SolarDataRecord):
    import pyarrow as pa
    import pyarrow.dataset as ds
    import uuid
    import os

    start = time.time()
    table = catalog.load_table("default.solar_data")

    # Convert to Arrow table
    arrow_table = pa.Table.from_pylist([record.dict()])

    # Write temporary Parquet file
    temp_file = f"/tmp/{uuid.uuid4()}.parquet"
    ds.write_dataset(arrow_table, temp_file, format="parquet", basename_template="data-{i}.parquet")

    # Append the file
    table.append_files([temp_file])

    end = time.time()
    os.remove(temp_file)

    return {
        "message": "Record appended",
        "time_seconds": round(end - start, 3)
    }