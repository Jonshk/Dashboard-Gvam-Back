from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import jwt
from datetime import datetime, timedelta
import bcrypt  # Importa bcrypt
from models import UserLogin, UserRegister
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
from database import get_db

auth_router = APIRouter()

@auth_router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe
    existing = db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    # Para registrar un usuario normal, podrías decidir si guardar la contraseña en texto plano o hashearla.
    # Aquí se guarda en texto plano (NO RECOMENDADO en producción).
    db.execute(
        text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"),
        {"username": user.username, "password": user.password, "role": "user"}
    )
    db.commit()
    return {"message": "Usuario registrado exitosamente."}

@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT id, password FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()
    if result is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    user_id, db_password = result

    # Verificar la contraseña:
    # Si la contraseña almacenada está hasheada (por ejemplo, cuando se crea un admin),
    # usamos bcrypt.checkpw para comparar
    if not bcrypt.checkpw(user.password.encode('utf-8'), db_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    payload = {
        "user_id": user_id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"token": token}

@auth_router.post("/register-admin")
def register_admin(user: UserRegister, db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe
    existing = db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    # Hashea la contraseña antes de insertar
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Inserta el usuario con rol 'admin'
    db.execute(
        text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"),
        {"username": user.username, "password": hashed_password, "role": "admin"}
    )
    db.commit()
    return {"message": "Administrador registrado exitosamente."}
