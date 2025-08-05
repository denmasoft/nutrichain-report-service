from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.orm import Session
from datetime importdatetime

from app.db.session import get_db
from app.schemas.report import (
    ReportRequest, StockReportResponse, MovementReportResponse, OrderReportResponse,
    AuditInfo
)
from app.services.report_service import report_service
from app.core.security import get_current_user, User
from app.core.idempotency import handle_idempotency

router = APIRouter()

@router.get(
    "/stock",
    response_model=StockReportResponse,
    summary="Generate Current Stock Report",
    description="Provides a snapshot of the current stock for all products."
)
def get_stock_report(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str = Depends(handle_idempotency),
):
    """
    Endpoint to generate stock repot.
    - **Security**: Requires a valid JWT.
    - **Idempotency**: Use `Idempotency-Key` header.
    """
    data = report_service.get_stock_report(db)
    
    response_data = StockReportResponse(
        metadata=AuditInfo(requested_by=current_user.username),
        data=data,
        date_range=None #
    )
    return response_data

@router.post(
    "/movements",
    response_model=MovementReportResponse,
    summary="Generate Inventory Movements Report",
    description="Provides a report of all inventory entries and exits within a given time range."
)
def get_movements_report(
    request: Request,
    report_request: ReportRequest = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str = Depends(handle_idempotency),
):
    """
    Endpoint to generate movement report.
    - **Security**: Requires a valid JWT.
    - **Idempotency**: Use `Idempotency-Key` header.
    """
    data = report_service.get_movements_report(db, report_request)
    
    response_data = MovementReportResponse(
        metadata=AuditInfo(requested_by=current_user.username),
        date_range=report_request,
        data=data
    )
    return response_data

@router.post(
    "/orders",
    response_model=OrderReportResponse,
    summary="Generate Orders Report",
    description="Provides a report of all orders created within a given time range."
)
def get_orders_report(
    request: Request,
    report_request: ReportRequest = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str = Depends(handle_idempotency),
):
    """
    Endpoint to generate order report.
    - **Security**: Requires a valid JWT.
    - **Idempotency**: Use `Idempotency-Key` header.
    """
    data = report_service.get_orders_report(db, report_request)
    
    response_data = OrderReportResponse(
        metadata=AuditInfo(requested_by=current_user.username),
        date_range=report_request,
        data=data
    )
    return response_data