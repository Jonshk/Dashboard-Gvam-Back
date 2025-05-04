from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.centers import CenterCreate, CenterRead, CenterUpdate
from models import Center as CenterModel

centers_router = APIRouter(prefix="/centers", tags=["centers"])

@centers_router.post("/", response_model=CenterRead, status_code=status.HTTP_201_CREATED)
def create_center(payload: CenterCreate, db: Session = Depends(get_db)):
    db_center = CenterModel(center=payload.center, phonenumber=payload.phonenumber)
    db.add(db_center)
    db.commit()
    db.refresh(db_center)
    return db_center

@centers_router.get("/{center_id}", response_model=CenterRead)
def read_center(center_id: int, db: Session = Depends(get_db)):
    db_center = db.query(CenterModel).filter(CenterModel.id == center_id).first()
    if not db_center:
        raise HTTPException(status_code=404, detail="Center not found")
    return db_center

@centers_router.get("/", response_model=list[CenterRead])
def list_centers(db: Session = Depends(get_db)):
    return db.query(CenterModel).all()

@centers_router.put("/{center_id}", response_model=CenterRead)
def update_center(center_id: int, payload: CenterUpdate, db: Session = Depends(get_db)):
    db_center = db.query(CenterModel).filter(CenterModel.id == center_id).first()
    if not db_center:
        raise HTTPException(status_code=404, detail="Center not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(db_center, field, value)
    db.commit()
    db.refresh(db_center)
    return db_center

@centers_router.delete("/{center_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_center(center_id: int, db: Session = Depends(get_db)):
    deleted = db.query(CenterModel).filter(CenterModel.id == center_id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Center not found")
    db.commit()
    return
