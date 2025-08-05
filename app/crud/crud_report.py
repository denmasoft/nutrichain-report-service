from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.report import ReportRequest

def get_stock_report_data(db: Session):
    query = text("""
        SELECT
            p.id as product_id,
            p.name as product_name,
            p.code as product_code,
            si.quantity,
            si.location,
            si.updated_at as last_updated
        FROM stock_items si
        JOIN products p ON si.product_id = p.id
        WHERE si.quantity > 0
        ORDER BY p.name;
    """)
    result = db.execute(query)
    return result.mappings().all()


def get_inventory_movements_data(db: Session, report_request: ReportRequest):
    query = text("""
        SELECT
            im.id as movement_id,
            p.id as product_id,
            p.name as product_name,
            im.type,
            im.quantity,
            im.created_at as movement_date,
            im.user
        FROM inventory_movements im
        JOIN products p ON im.product_id = p.id
        WHERE im.created_at BETWEEN :start_date AND :end_date
        ORDER BY im.created_at DESC;
    """)
    result = db.execute(query, {"start_date": report_request.start_date, "end_date": report_request.end_date})
    return result.mappings().all()

def get_orders_report_data(db: Session, report_request: ReportRequest):
    query = text("""
        SELECT
            o.id as order_id,
            o.status,
            o.created_at as order_date,
            (SELECT SUM(oi.quantity) FROM order_items oi WHERE oi.order_id = o.id) as total_items
        FROM orders o
        WHERE o.created_at BETWEEN :start_date AND :end_date
        ORDER BY o.created_at DESC;
    """)
    result = db.execute(query, {"start_date": report_request.start_date, "end_date": report_request.end_date})
    return result.mappings().all()