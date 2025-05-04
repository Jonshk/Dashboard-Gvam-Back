# schemas/receptions.py
from pydantic import BaseModel, Field
from datetime import date
from typing import List

class ReceptionItemCreate(BaseModel):
    product_name: str = Field(..., example="Ratón")
    quantity: int     = Field(..., example=5)

class ReceptionCreate(BaseModel):
    center_id: int        = Field(..., example=1)
    reception_date: date  = Field(..., example="2025-03-29")
    items: List[ReceptionItemCreate]

class ReceptionItemRead(ReceptionItemCreate):
    reception_id: int

    class Config:
        from_attributes = True  # mapea desde el atributo ORM

class ReceptionRead(BaseModel):
    id: int
    center_id: int
    reception_date: date
    items: List[ReceptionItemRead]

    class Config:
        from_attributes = True
