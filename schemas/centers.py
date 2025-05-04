from pydantic import BaseModel, Field

class CenterBase(BaseModel):
    center: str      = Field(..., example="Centro A")
    phonenumber: str = Field(..., example="+34123456789")

class CenterCreate(CenterBase): pass
class CenterUpdate(CenterBase): pass

class CenterRead(CenterBase):
    id: int
    class Config:
        orm_mode = True

# — stock del centro
class CenterStockBase(BaseModel):
    product_name: str           = Field(..., example="Monitor 24\"")
    quantity:     int           = Field(..., example=10)
    price:        float         = Field(..., example=199.99)
    image_path:   str | None    = Field(None, example="images/monitor.png")
    category:     str           = Field(..., example="consumible")
    estado:       str | None    = Field(None, example="Operativo")

class CenterStockCreate(CenterStockBase): pass
class CenterStockUpdate(CenterStockBase): pass

class CenterStockRead(CenterStockBase):
    id: int
    center_id: int
    class Config:
        orm_mode = True
