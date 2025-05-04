# endpoints/centers.py

from fastapi import (
    APIRouter, Depends, HTTPException, status,
    UploadFile, File
)
from sqlalchemy.orm import Session
from typing import List

import pandas as pd

from database import get_db
from models import Center as CenterModel, CenterStock as CenterStockModel
from schemas.centers import (
    CenterCreate, CenterRead, CenterUpdate,
    CenterStockCreate, CenterStockRead, CenterStockUpdate
)

router = APIRouter(
    
    tags=["centers"],
    responses={404: {"description": "Not found"}}
)

# — CRUD Centros — #

@router.post(
    "/",
    response_model=CenterRead,
    status_code=status.HTTP_201_CREATED
)
def create_center(
    payload: CenterCreate,
    db: Session = Depends(get_db)
):
    db_center = CenterModel(
        center=payload.center,
        phonenumber=payload.phonenumber
    )
    db.add(db_center)
    db.commit()
    db.refresh(db_center)
    return db_center


@router.get(
    "/",
    response_model=List[CenterRead]
)
def list_centers(db: Session = Depends(get_db)):
    return db.query(CenterModel).all()


@router.get(
    "/{center_id}",
    response_model=CenterRead
)
def read_center(
    center_id: int,
    db: Session = Depends(get_db)
):
    c = db.query(CenterModel).get(center_id)
    if not c:
        raise HTTPException(404, "Center not found")
    return c


@router.put(
    "/{center_id}",
    response_model=CenterRead
)
def update_center(
    center_id: int,
    payload: CenterUpdate,
    db: Session = Depends(get_db)
):
    c = db.query(CenterModel).get(center_id)
    if not c:
        raise HTTPException(404, "Center not found")
    for field, val in payload.dict(exclude_unset=True).items():
        setattr(c, field, val)
    db.commit()
    db.refresh(c)
    return c


@router.delete(
    "/{center_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_center(
    center_id: int,
    db: Session = Depends(get_db)
):
    deleted = db.query(CenterModel).filter_by(id=center_id).delete()
    if not deleted:
        raise HTTPException(404, "Center not found")
    db.commit()


# — CRUD Inventario por Centro — #

@router.get(
    "/{center_id}/inventory",
    response_model=List[CenterStockRead]
)
def list_inventory(
    center_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(CenterStockModel)
          .filter_by(center_id=center_id)
          .all()
    )


@router.post(
    "/{center_id}/inventory",
    response_model=CenterStockRead,
    status_code=status.HTTP_201_CREATED
)
def add_inventory(
    center_id: int,
    payload: CenterStockCreate,
    db: Session = Depends(get_db)
):
    stock = CenterStockModel(
        center_id=center_id,
        **payload.dict()
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@router.put(
    "/inventory/{stock_id}",
    response_model=CenterStockRead
)
def update_inventory(
    stock_id: int,
    payload: CenterStockUpdate,
    db: Session = Depends(get_db)
):
    stock = db.query(CenterStockModel).get(stock_id)
    if not stock:
        raise HTTPException(404, "Inventory item not found")
    for field, val in payload.dict(exclude_unset=True).items():
        setattr(stock, field, val)
    db.commit()
    db.refresh(stock)
    return stock


@router.delete(
    "/inventory/{stock_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_inventory(
    stock_id: int,
    db: Session = Depends(get_db)
):
    deleted = (
        db.query(CenterStockModel)
          .filter_by(id=stock_id)
          .delete()
    )
    if not deleted:
        raise HTTPException(404, "Inventory item not found")
    db.commit()


# — Importar Excel al Inventario — #

@router.post(
    "/{center_id}/inventory/import",
    status_code=status.HTTP_201_CREATED
)
def import_inventory_excel(
    center_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Recibe un Excel con columnas:
      - Producto, Cantidad, Precio, Categoría, Estado (opcional)
    y añade esas filas al inventory del centro.
    """
    df = pd.read_excel(file.file)
    imported = 0
    for _, row in df.iterrows():
        stock = CenterStockModel(
            center_id    = center_id,
            product_name = str(row['Producto']).strip(),
            quantity     = int(row['Cantidad']),
            price        = float(row['Precio']),
            category     = str(row['Categoría']).strip().lower(),
            estado       = (None if pd.isna(row.get('Estado')) else str(row['Estado']).strip())
        )
        db.add(stock)
        imported += 1
    db.commit()
    return {"imported": imported}
