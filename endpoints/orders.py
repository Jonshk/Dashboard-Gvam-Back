# backend/endpoints/orders.py

from fastapi            import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm     import Session
from database           import get_db
from models             import Order as OrderModel, OrderItem as OrderItemModel, Center as CenterModel
from schemas.orders     import Order as OrderSchema, OrderCreate as OrderCreateSchema, OrderUpdate as OrderUpdateSchema
from typing             import List
from sqlalchemy.exc     import IntegrityError

router = APIRouter(tags=["orders"])

@router.get("/", response_model=List[OrderSchema])
def list_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()

@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(o: OrderCreateSchema, db: Session = Depends(get_db)):
    if not db.query(CenterModel).filter(CenterModel.id == o.center_id).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Center not found")
    order = OrderModel(
        center_id        = o.center_id,
        shipping_company = o.shipping_company,
        order_date       = o.order_date,
        status           = o.status or "Pendiente",
        comments         = o.comments
    )
    order.items = [
        OrderItemModel(product_name=i.product_name, quantity=i.quantity)
        for i in o.items
    ]
    try:
        db.add(order)
        db.commit()
        db.refresh(order)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
    return order

@router.get("/{order_id}", response_model=OrderSchema)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=OrderSchema)
def update_order(order_id: int, o: OrderUpdateSchema, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")
    for field, value in o.dict(exclude_unset=True).items():
        if field == "items":
            order.items.clear()
            order.items = [
                OrderItemModel(product_name=i.product_name, quantity=i.quantity)
                for i in value
            ]
        else:
            setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.delete(order)
    db.commit()

__all__ = ["router"]
