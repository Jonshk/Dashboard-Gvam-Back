# endpoints/repairs.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Repair, RepairItem
from schemas.repairs import (
    RepairCreate,
    RepairRead,
    RepairItemCreate,
    RepairItemRead
)

repairs_router = APIRouter()

# — Listar reparaciones
@repairs_router.get("/repairs", response_model=list[RepairRead])
def list_repairs(db: Session = Depends(get_db)):
    return db.query(Repair).all()

# — Obtener una reparación por ID
@repairs_router.get("/repairs/{repair_id}", response_model=RepairRead)
def read_repair(repair_id: int, db: Session = Depends(get_db)):
    repair = db.query(Repair).filter(Repair.id == repair_id).first()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    return repair

# — Crear una nueva reparación
@repairs_router.post(
    "/repairs",
    response_model=RepairRead,
    status_code=status.HTTP_201_CREATED
)
def create_repair(r: RepairCreate, db: Session = Depends(get_db)):
    # Creamos la cabecera de la reparación
    repair = Repair(
        center_id=r.center_id,
        repair_type=r.repair_type,
        repair_date=r.repair_date
    )
    db.add(repair)
    db.commit()
    db.refresh(repair)

    # Añadimos cada item asociado a esa reparación
    for item in r.items:
        ri = RepairItem(
            repair_id=repair.id,
            product_name=item.product_name,
            repair_quantity=item.repair_quantity
        )
        db.add(ri)
    db.commit()
    db.refresh(repair)
    return repair

# — Actualizar una reparación existente
@repairs_router.put("/repairs/{repair_id}", response_model=RepairRead)
def update_repair(
    repair_id: int,
    r: RepairCreate,
    db: Session = Depends(get_db)
):
    repair = db.query(Repair).filter(Repair.id == repair_id).first()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")

    # Actualizamos campos
    repair.center_id   = r.center_id
    repair.repair_type = r.repair_type
    repair.repair_date = r.repair_date
    db.commit()

    # Reemplazamos items antiguos por los nuevos
    db.query(RepairItem).filter(RepairItem.repair_id == repair.id).delete()
    for item in r.items:
        ri = RepairItem(
            repair_id=repair.id,
            product_name=item.product_name,
            repair_quantity=item.repair_quantity
        )
        db.add(ri)
    db.commit()
    db.refresh(repair)
    return repair

# — Eliminar una reparación
@repairs_router.delete(
    "/repairs/{repair_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_repair(repair_id: int, db: Session = Depends(get_db)):
    repair = db.query(Repair).filter(Repair.id == repair_id).first()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    db.delete(repair)
    db.commit()
