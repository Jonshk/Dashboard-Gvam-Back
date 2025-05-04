# schemas/repairs.py
from pydantic import BaseModel, Field
from typing import List
from datetime import date

class RepairItemCreate(BaseModel):
    product_name: str       = Field(..., example="Teclado")
    repair_quantity: int    = Field(..., example=1)

class RepairCreate(BaseModel):
    center_id: int          = Field(..., example=1)
    repair_type: str        = Field(..., example="Mantenimiento")
    repair_date: date       = Field(..., example="2025-03-29")
    items: List[RepairItemCreate]

class RepairItemRead(RepairItemCreate):
    repair_id: int

    class Config:
        from_attributes = True

class RepairRead(BaseModel):
    id: int
    center_id: int
    repair_type: str
    repair_date: date
    items: List[RepairItemRead]

    class Config:
        from_attributes = True
