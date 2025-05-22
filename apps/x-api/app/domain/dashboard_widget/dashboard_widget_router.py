from fastapi import APIRouter, HTTPException, status
from typing import List
from http import HTTPStatus

from common_fastapi import ResourceNotFoundException
from .dashboard_widget_service import DashboardWidgetService
from .dashboard_widget_dto import DashboardWidgetResult, DashboardWidgetCreateForm

dashboard_widget_router = APIRouter(prefix="/dashboard-widget", tags=["DashboardWidget"])
service = DashboardWidgetService()

@dashboard_widget_router.post("/", status_code=HTTPStatus.CREATED)
async def create_dashboard_widget():
    """
    Initialize the DashboardWidget collection from windmill.json
    """
    await service.create()
    return {"message": "DashboardWidget collection created and populated"}

@dashboard_widget_router.get("/", response_model=List[DashboardWidgetResult])
async def read_dashboard_widgets():
    """Retrieve all dashboard widgets"""
    return await service.find_all()

@dashboard_widget_router.get("/{uid}", response_model=DashboardWidgetResult)
async def read_dashboard_widget(uid: str):
    """Retrieve a single dashboard widget by ID"""
    try:
        return await service.find_one(uid)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@dashboard_widget_router.put("/{uid}", response_model=DashboardWidgetResult)
async def update_dashboard_widget(uid: str, form: DashboardWidgetCreateForm):
    """Update a dashboard widget by ID"""
    try:
        return await service.update(uid, form)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@dashboard_widget_router.delete("/{uid}", status_code=HTTPStatus.NO_CONTENT)
async def delete_dashboard_widget(uid: str):
    """Delete a dashboard widget by ID"""
    try:
        await service.remove(uid)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

@dashboard_widget_router.delete("/", status_code=HTTPStatus.NO_CONTENT)
async def delete_all_dashboard_widgets():
    """Truncate the DashboardWidget collection"""
    await service.remove_all()