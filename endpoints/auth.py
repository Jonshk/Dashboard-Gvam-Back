from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt, jwt
from datetime import datetime, timedelta

from schemas.auth import UserRegister, UserLogin
from models import User            # <-- modelo ORM que creamos arriba
from config import settings
from database import get_db

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(400, "El usuario ya existe.")

    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    db_user = User(username=user.username, password=hashed, role="user")
    db.add(db_user)
    db.commit()
    return {"message": "Usuario registrado exitosamente."}

@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not bcrypt.checkpw(user.password.encode(), db_user.password.encode()):
        raise HTTPException(401, "Credenciales inválidas.")

    payload = {
        "user_id":  db_user.id,
        "username": db_user.username,
        "exp":      datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return {
        "data": {
            "email": db_user.username,
            "role":  db_user.role,
            "tokens": {
                "accessToken":  token,
                "refreshToken": token
            }
        }
    }
