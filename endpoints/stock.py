# endpoints/stock.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import StockCategory as StockCategoryModel, \
                   StockSubcategory as StockSubcategoryModel, \
                   StockItem as StockItemModel
from schemas.stock import (
    StockCategory as StockCategorySchema,
    StockSubcategory as StockSubcategorySchema,
    StockItemCreate,
    StockItemRead
)

stock_router = APIRouter()

# — Categories CRUD

@stock_router.get(
    "/categories",
    response_model=list[StockCategorySchema]
)
def list_categories(db: Session = Depends(get_db)):
    return db.query(StockCategoryModel).all()


@stock_router.get(
    "/categories/{category_id}",
    response_model=StockCategorySchema
)
def read_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(StockCategoryModel).get(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat


@stock_router.post(
    "/categories",
    response_model=StockCategorySchema,
    status_code=status.HTTP_201_CREATED
)
def create_category(c: StockCategorySchema, db: Session = Depends(get_db)):
    cat = StockCategoryModel(name=c.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@stock_router.put(
    "/categories/{category_id}",
    response_model=StockCategorySchema
)
def update_category(
    category_id: int,
    c: StockCategorySchema,
    db: Session = Depends(get_db)
):
    cat = db.query(StockCategoryModel).get(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.name = c.name
    db.commit()
    db.refresh(cat)
    return cat


@stock_router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(StockCategoryModel).get(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()


# — Subcategories CRUD

@stock_router.get(
    "/subcategories",
    response_model=list[StockSubcategorySchema]
)
def list_subcategories(db: Session = Depends(get_db)):
    return db.query(StockSubcategoryModel).all()


@stock_router.get(
    "/subcategories/{sub_id}",
    response_model=StockSubcategorySchema
)
def read_subcategory(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(StockSubcategoryModel).get(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return sub


@stock_router.post(
    "/subcategories",
    response_model=StockSubcategorySchema,
    status_code=status.HTTP_201_CREATED
)
def create_subcategory(
    s: StockSubcategorySchema,
    db: Session = Depends(get_db)
):
    sub = StockSubcategoryModel(category_id=s.category_id, name=s.name)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


@stock_router.put(
    "/subcategories/{sub_id}",
    response_model=StockSubcategorySchema
)
def update_subcategory(
    sub_id: int,
    s: StockSubcategorySchema,
    db: Session = Depends(get_db)
):
    sub = db.query(StockSubcategoryModel).get(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    sub.name = s.name
    sub.category_id = s.category_id
    db.commit()
    db.refresh(sub)
    return sub


@stock_router.delete(
    "/subcategories/{sub_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_subcategory(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(StockSubcategoryModel).get(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    db.delete(sub)
    db.commit()


# — Items CRUD

@stock_router.get(
    "/items",
    response_model=list[StockItemRead]
)
def list_items(db: Session = Depends(get_db)):
    return db.query(StockItemModel).all()


@stock_router.get(
    "/items/{item_id}",
    response_model=StockItemRead
)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(StockItemModel).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@stock_router.post(
    "/items",
    response_model=StockItemRead,
    status_code=status.HTTP_201_CREATED
)
def create_item(
    i: StockItemCreate,
    db: Session = Depends(get_db)
):
    item = StockItemModel(
        subcategory_id=i.subcategory_id,
        product_name=i.product_name,
        quantity=i.quantity,
        price=i.price,
        image_path=i.image_path,
        estado=i.estado
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@stock_router.put(
    "/items/{item_id}",
    response_model=StockItemRead
)
def update_item(
    item_id: int,
    i: StockItemCreate,
    db: Session = Depends(get_db)
):
    item = db.query(StockItemModel).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.subcategory_id = i.subcategory_id
    item.product_name   = i.product_name
    item.quantity       = i.quantity
    item.price          = i.price
    item.image_path     = i.image_path
    item.estado         = i.estado
    db.commit()
    db.refresh(item)
    return item


@stock_router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(StockItemModel).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
