from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Order, OrderItem
from schemas.orders import Order as OrderSchema, OrderItem as OrderItemSchema
orders_router = APIRouter()

# — Listar todas las órdenes
@orders_router.get("/", response_model=list[OrderSchema])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

# — Leer una orden por ID
@orders_router.get("/{order_id}", response_model=OrderSchema)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# — Crear orden
@orders_router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(o: OrderSchema, db: Session = Depends(get_db)):
    order = Order(
        center_id=o.center_id,
        shipping_company=o.shipping_company,
        order_date=o.order_date,
        items=[OrderItem(product_name=i.product_name, quantity=i.quantity) for i in o.items]
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

# — Actualizar orden
@orders_router.put("/{order_id}", response_model=OrderSchema)
def update_order(order_id: int, o: OrderSchema, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # campos simples
    order.center_id = o.center_id
    order.shipping_company = o.shipping_company
    order.order_date = o.order_date
    # replace items
    order.items.clear()
    for i in o.items:
        order.items.append(OrderItem(product_name=i.product_name, quantity=i.quantity))
    db.commit()
    db.refresh(order)
    return order

# — Eliminar orden
@orders_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
