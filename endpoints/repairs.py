# endpoints/repairs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Repair
from database import get_db

repairs_router = APIRouter()

@repairs_router.get("/")
def list_repairs(db: Session = Depends(get_db)):
    try:
        repairs = db.execute("SELECT * FROM repairs").fetchall()
        return {"data": repairs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@repairs_router.post("/")
def create_repair(repair: Repair, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            "INSERT INTO repairs (center_id, repair_type, repair_date) VALUES (:center_id, :repair_type, :repair_date) RETURNING id",
            {"center_id": repair.center_id, "repair_type": repair.repair_type, "repair_date": repair.repair_date}
        )
        repair_id = result.fetchone()[0]
        for item in repair.items:
            db.execute(
                "INSERT INTO repair_items (repair_id, product_name, repair_quantity) VALUES (:repair_id, :product_name, :repair_quantity)",
                {"repair_id": repair_id, "product_name": item.product_name, "repair_quantity": item.repair_quantity}
            )
        db.commit()
        return {"message": "Reparación creada exitosamente.", "repair_id": repair_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
