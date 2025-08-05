from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ReportRequest(BaseModel):
    start_date: datetime = Field(..., description="Start date for the report range (ISO 8601 format)")
    end_date: datetime = Field(..., description="End date for the report range (ISO 8601 format)")

class AuditInfo(BaseModel):
    requested_by: str
    requested_at: datetime = Field(default_factory=datetime.utcnow)

class StockReportItem(BaseModel):
    product_id: int
    product_name: str
    product_code: str
    quantity: int
    location: str
    last_updated: datetime

class StockReportResponse(BaseModel):
    metadata: AuditInfo
    report_type: str = "Stock Report"
    date_range: ReportRequest
    data: List[StockReportItem]

class MovementReportItem(BaseModel):
    movement_id: int
    product_id: int
    product_name: str
    type: str
    quantity: int
    movement_date: datetime
    user: str # Blameable

class MovementReportResponse(BaseModel):
    metadata: AuditInfo
    report_type: str = "Inventory Movement Report"
    date_range: ReportRequest
    data: List[MovementReportItem]

class OrderReportItem(BaseModel):
    order_id: int
    status: str
    total_items: int
    order_date: datetime

class OrderReportResponse(BaseModel):
    metadata: AuditInfo
    report_type: str = "Orders Report"
    date_range: ReportRequest
    data: List[OrderReportItem]