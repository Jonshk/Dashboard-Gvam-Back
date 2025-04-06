# models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Autenticación
class UserLogin(BaseModel):
    username: str = Field(..., example="admin@ejemplo.com")
    password: str = Field(..., example="admin123")

class UserRegister(BaseModel):
    username: str = Field(..., example="nuevo_usuario@ejemplo.com")
    password: str = Field(..., example="contraseña123")

# Producto
class Product(BaseModel):
    id: Optional[int]
    product_name: str = Field(..., example="Monitor 24 pulgadas")
    quantity: int = Field(..., example=50)
    price: float = Field(..., example=199.99)
    image_path: Optional[str] = Field(None, example="images/monitor.png")
    category: Optional[str] = Field(None, example="consumible")
    estado: Optional[str] = Field(None, example="funcional")

# Orden
class OrderItem(BaseModel):
    product_name: str = Field(..., example="Monitor 24 pulgadas")
    quantity: int = Field(..., example=2)

class Order(BaseModel):
    id: Optional[int]
    center_id: int = Field(..., example=1)
    shipping_company: str = Field(..., example="DHL")
    order_date: date = Field(..., example="2025-03-29")
    items: List[OrderItem]

# Reparación
class RepairItem(BaseModel):
    product_name: str = Field(..., example="Teclado")
    repair_quantity: int = Field(..., example=1)

class Repair(BaseModel):
    id: Optional[int]
    center_id: int = Field(..., example=1)
    repair_type: str = Field(..., example="Mantenimiento")
    repair_date: date = Field(..., example="2025-03-29")
    items: List[RepairItem]

# Recepción
class ReceptionItem(BaseModel):
    product_name: str = Field(..., example="Ratón")
    quantity: int = Field(..., example=5)

class Reception(BaseModel):
    id: Optional[int]
    center_id: int = Field(..., example=1)
    reception_date: date = Field(..., example="2025-03-29")
    items: List[ReceptionItem]
