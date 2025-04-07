# init_admin.py
import bcrypt
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal

def initialize_admin():
    """
    Verifica si existe un usuario con rol 'admin'. Si no existe, lo crea.
    Credenciales de ejemplo:
      - Usuario: admin@ejemplo.com
      - Contraseña: admin123
    La contraseña se encripta usando bcrypt.
    """
    db: Session = SessionLocal()
    try:
        # Usamos text() para la consulta textual
        result = db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": "admin@ejemplo.com"}
        ).fetchone()

        if result is None:
            password = "admin123"
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            db.execute(
                text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"),
                {
                    "username": "admin@ejemplo.com",
                    "password": hashed.decode("utf-8"),
                    "role": "admin"
                }
            )
            db.commit()
            print("Usuario admin creado exitosamente.")
        else:
            print("El usuario admin ya existe.")
    except Exception as e:
        db.rollback()
        print("Error al inicializar usuario admin:", e)
    finally:
        db.close()
