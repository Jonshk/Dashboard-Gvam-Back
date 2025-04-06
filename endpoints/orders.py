# endpoints/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Order
from database import get_db

orders_router = APIRouter()

@orders_router.get("/")
def list_orders(db: Session = Depends(get_db)):
    try:
        orders = db.execute("SELECT * FROM orders").fetchall()
        return {"data": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@orders_router.post("/")
def create_order(order: Order, db: Session = Depends(get_db)):
    try:
        # Inserta en orders y luego en order_items
        result = db.execute(
            "INSERT INTO orders (center_id, shipping_company, order_date) VALUES (:center_id, :shipping_company, :order_date) RETURNING id",
            {"center_id": order.center_id, "shipping_company": order.shipping_company, "order_date": order.order_date}
        )
        order_id = result.fetchone()[0]
        for item in order.items:
            db.execute(
                "INSERT INTO order_items (order_id, product_name, quantity) VALUES (:order_id, :product_name, :quantity)",
                {"order_id": order_id, "product_name": item.product_name, "quantity": item.quantity}
            )
        db.commit()
        return {"message": "Orden creada exitosamente.", "order_id": order_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
