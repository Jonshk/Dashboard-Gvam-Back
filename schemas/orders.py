from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class OrderItemCreate(BaseModel):
    product_name: str = Field(..., example="Monitor")
    quantity: int = Field(..., example=2)

class OrderItem(OrderItemCreate):
    order_id: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    center_id: int = Field(..., example=1)
    shipping_company: str = Field(..., example="DHL")
    order_date: date = Field(..., example="2025-05-03")
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    shipping_company: Optional[str]
    order_date: Optional[date]

class Order(BaseModel):
    id: int
    center_id: int
    shipping_company: str
    order_date: date
    items: List[OrderItem]

    class Config:
        from_attributes = True
