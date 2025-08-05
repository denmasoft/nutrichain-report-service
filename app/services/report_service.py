from sqlalchemy.orm import Session
from app.crud import crud_report
from app.schemas.report import ReportRequest

class ReportService:
    def get_stock_report(self, db: Session):
        """Service to generate the current stock report."""
        return crud_report.get_stock_report_data(db)

    def get_movements_report(self, db: Session, report_request: ReportRequest):
        """Service to generate the inventory movements report."""
        return crud_report.get_inventory_movements_data(db, report_request)

    def get_orders_report(self, db: Session, report_request: ReportRequest):
        """Service to generate the orders report."""
        return crud_report.get_orders_report_data(db, report_request)

report_service = ReportService()