# endpoints/receptions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Reception
from database import get_db

receptions_router = APIRouter()

@receptions_router.get("/")
def list_receptions(db: Session = Depends(get_db)):
    try:
        receptions = db.execute("SELECT * FROM receptions").fetchall()
        return {"data": receptions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@receptions_router.post("/")
def create_reception(reception: Reception, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            "INSERT INTO receptions (center_id, reception_date) VALUES (:center_id, :reception_date) RETURNING id",
            {"center_id": reception.center_id, "reception_date": reception.reception_date}
        )
        reception_id = result.fetchone()[0]
        for item in reception.items:
            db.execute(
                "INSERT INTO reception_items (reception_id, product_name, quantity) VALUES (:reception_id, :product_name, :quantity)",
                {"reception_id": reception_id, "product_name": item.product_name, "quantity": item.quantity}
            )
        db.commit()
        return {"message": "Recepción creada exitosamente.", "reception_id": reception_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
