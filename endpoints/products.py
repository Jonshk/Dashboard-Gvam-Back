# endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
from database import get_db

products_router = APIRouter()

@products_router.get("/")
def list_products(db: Session = Depends(get_db)):
    try:
        products = db.execute("SELECT * FROM stock").fetchall()
        return {"data": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@products_router.post("/")
def create_product(product: Product, db: Session = Depends(get_db)):
    try:
        db.execute(
            "INSERT INTO stock (product_name, quantity, price, image_path, category, estado) VALUES (:product_name, :quantity, :price, :image_path, :category, :estado)",
            product.dict()
        )
        db.commit()
        return {"message": "Producto creado exitosamente."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
