# schemas/stock.py

from pydantic import BaseModel, Field
from typing import Optional, List


# ——— Categorías ———

class StockCategoryBase(BaseModel):
    name: str = Field(..., example="Repuestos")


class StockCategory(StockCategoryBase):
    id: int

    class Config:
        from_attributes = True


# ——— Subcategorías ———

class StockSubcategoryBase(BaseModel):
    category_id: int = Field(..., example=1)
    name: str        = Field(..., example="Baterías")


class StockSubcategory(StockSubcategoryBase):
    id: int

    class Config:
        from_attributes = True


# ——— Ítems ———

class StockItemCreate(BaseModel):
    subcategory_id: int         = Field(..., example=1)
    product_name: str           = Field(..., example="Monitor 24\"")
    quantity: int               = Field(..., example=10)
    price: float                = Field(..., example=199.99)
    image_path: Optional[str]   = Field(None, example="images/monitor.png")
    estado: Optional[str]       = Field(None, example="funcional")


class StockItemRead(StockItemCreate):
    id: int

    class Config:
        from_attributes = True
