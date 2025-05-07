from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Query
from typing import List as _list

from common_fastapi import ResourceNotFoundException
from .solar_panel_service import SolarPanelService
from .solar_panel_dto import SolarPanelResult, SolarPanelCreateForm

solar_panel_router = APIRouter(prefix="/solar-panel", tags=["SolarPanel"])
service = SolarPanelService()

@solar_panel_router.post("/", status_code=HTTPStatus.CREATED)
async def create_solar_panel():
    """Create the joined solar_panel.parquet by combining information and location data."""
    service.create()
    return {"message": "solar_panel.parquet created successfully"}

@solar_panel_router.get("/", response_model=_list[SolarPanelResult])
async def read_solar_panels():
    """Retrieve all solar panel records."""
    return service.find_all()

@solar_panel_router.get("/paginated", response_model=_list[SolarPanelResult])
async def read_solar_panels_paginated(
    limit: int = Query(50, ge=1),
    page_number: int = Query(1, ge=1, alias="pageNumber")
):
    """Retrieve paginated solar panel records."""
    return service.find_all_by_pagination(limit, page_number)

@solar_panel_router.get("/{uid}", response_model=SolarPanelResult)
async def read_solar_panel(uid: int):
    """Retrieve a solar panel record by ID."""
    try:
        return service.find_one(uid)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@solar_panel_router.put("/{uid}", response_model=SolarPanelResult)
async def update_solar_panel(uid: int, form: SolarPanelCreateForm):
    """Update a solar panel record by ID."""
    try:
        return service.update(uid, form)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@solar_panel_router.delete("/{uid}", status_code=HTTPStatus.NO_CONTENT)
async def delete_solar_panel(uid: int):
    """Delete a solar panel record by ID."""
    try:
        service.remove(uid)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@solar_panel_router.delete("/", status_code=HTTPStatus.NO_CONTENT)
async def delete_all_solar_panels():
    """Delete the entire solar_panel.parquet file."""
    service.remove_all()

# from http import HTTPStatus
# from fastapi import APIRouter, HTTPException
# from typing import List as _list

# from common_fastapi import ResourceNotFoundException
# from .solar_panel_service import SolarPanelService
# from .solar_panel_dto import SolarPanelResult, SolarPanelCreateForm

# solar_panel_router = APIRouter(prefix="/solar-panel", tags=["SolarPanel"])
# service = SolarPanelService()

# @solar_panel_router.post("/", status_code=HTTPStatus.CREATED)
# async def create_solar_panel():
#     """
#     Create the joined solar_panel.parquet by combining information and location data.
#     """
#     service.create()
#     return {"message": "solar_panel.parquet created successfully"}

# @solar_panel_router.get("/", response_model=_list[SolarPanelResult])
# async def read_solar_panels():
#     """Retrieve all solar panel records."""
#     return service.find_all()

# @solar_panel_router.get("/{uid}", response_model=SolarPanelResult)
# async def read_solar_panel(uid: int):
#     """Retrieve a solar panel record by ID."""
#     try:
#         return service.find_one(uid)
#     except ResourceNotFoundException as e:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

# @solar_panel_router.put("/{uid}", response_model=SolarPanelResult)
# async def update_solar_panel(uid: int, form: SolarPanelCreateForm):
#     """Update a solar panel record by ID."""
#     try:
#         return service.update(uid, form)
#     except ResourceNotFoundException as e:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

# @solar_panel_router.delete("/{uid}", status_code=HTTPStatus.NO_CONTENT)
# async def delete_solar_panel(uid: int):
#     """Delete a solar panel record by ID."""
#     try:
#         service.remove(uid)
#     except ResourceNotFoundException as e:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

# @solar_panel_router.delete("/", status_code=HTTPStatus.NO_CONTENT)
# async def delete_all_solar_panels():
#     """Delete the entire solar_panel.parquet file."""
#     service.remove_all()