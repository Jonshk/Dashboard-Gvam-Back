from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
import bcrypt
import jwt

from models import UserLogin, UserRegister
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
from database import get_db

auth_router = APIRouter()

@auth_router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    db.execute(
        text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"),
        {"username": user.username, "password": hashed_password, "role": "user"}
    )
    db.commit()
    return {"message": "Usuario registrado exitosamente."}


@auth_router.post("/register-admin")
def register_admin(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    db.execute(
        text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"),
        {"username": user.username, "password": hashed_password, "role": "admin"}
    )
    db.commit()
    return {"message": "Administrador registrado exitosamente."}


@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT id, username, password, role FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()

    if result is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    user_id, db_username, db_password, role = result

    if not bcrypt.checkpw(user.password.encode("utf-8"), db_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    payload = {
        "user_id": user_id,
        "username": db_username,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "data": {
            "email": db_username,
            "role": role,
            "tokens": {
                "accessToken": access_token,
                "refreshToken": access_token  # Puedes usar uno distinto si implementas refresh real
            }
        }
    }
