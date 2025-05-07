# backend/schemas/orders.py

from datetime import date
from typing      import List, Optional
from pydantic    import BaseModel

class OrderItem(BaseModel):
    product_name: str
    quantity:     int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    center_id:        int
    shipping_company: str
    order_date:       date
    status:           Optional[str] = "Pendiente"
    comments:         Optional[str] = None
    items:            List[OrderItem]

    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    shipping_company: Optional[str]
    order_date:       Optional[date]
    status:           Optional[str]
    comments:         Optional[str]
    items:            Optional[List[OrderItem]]

    class Config:
        orm_mode = True

class Order(OrderBase):
    id: int
