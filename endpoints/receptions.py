# endpoints/receptions.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Reception, ReceptionItem
from schemas.receptions import (
    ReceptionCreate,
    ReceptionRead,
    ReceptionItemCreate,
    ReceptionItemRead
)

receptions_router = APIRouter()

# — Listar recepciones
@receptions_router.get("/receptions", response_model=list[ReceptionRead])
def list_receptions(db: Session = Depends(get_db)):
    return db.query(Reception).all()

# — Obtener una recepción por ID
@receptions_router.get("/receptions/{reception_id}", response_model=ReceptionRead)
def read_reception(reception_id: int, db: Session = Depends(get_db)):
    rec = db.query(Reception).filter(Reception.id == reception_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Reception not found")
    return rec

# — Crear una nueva recepción
@receptions_router.post(
    "/receptions",
    response_model=ReceptionRead,
    status_code=status.HTTP_201_CREATED
)
def create_reception(r: ReceptionCreate, db: Session = Depends(get_db)):
    reception = Reception(
        center_id=r.center_id,
        reception_date=r.reception_date
    )
    db.add(reception)
    db.commit()
    db.refresh(reception)

    for item in r.items:
        ri = ReceptionItem(
            reception_id=reception.id,
            product_name=item.product_name,
            quantity=item.quantity
        )
        db.add(ri)
    db.commit()
    db.refresh(reception)
    return reception

# — Actualizar una recepción existente
@receptions_router.put("/receptions/{reception_id}", response_model=ReceptionRead)
def update_reception(
    reception_id: int,
    r: ReceptionCreate,
    db: Session = Depends(get_db)
):
    rec = db.query(Reception).filter(Reception.id == reception_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Reception not found")

    rec.center_id      = r.center_id
    rec.reception_date = r.reception_date
    db.commit()

    db.query(ReceptionItem).filter(ReceptionItem.reception_id == rec.id).delete()
    for item in r.items:
        ri = ReceptionItem(
            reception_id=rec.id,
            product_name=item.product_name,
            quantity=item.quantity
        )
        db.add(ri)
    db.commit()
    db.refresh(rec)
    return rec

# — Eliminar una recepción
@receptions_router.delete(
    "/receptions/{reception_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_reception(reception_id: int, db: Session = Depends(get_db)):
    rec = db.query(Reception).filter(Reception.id == reception_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Reception not found")
    db.delete(rec)
    db.commit()
