# endpoints/reports.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

reports_router = APIRouter()

@reports_router.get("/")
def generate_report(db: Session = Depends(get_db), start_date: str = "2025-01-01", end_date: str = "2025-12-31"):
    try:
        # Ejemplo: Suma total de órdenes en un rango de fechas
        result = db.execute(
            "SELECT SUM(oi.quantity * s.price) as total_gasto "
            "FROM orders o "
            "INNER JOIN order_items oi ON o.id = oi.order_id "
            "INNER JOIN stock s ON oi.product_name = s.product_name "
            "WHERE o.order_date BETWEEN :start_date AND :end_date",
            {"start_date": start_date, "end_date": end_date}
        ).fetchone()
        total = result[0] if result[0] is not None else 0
        return {"total_gasto": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
