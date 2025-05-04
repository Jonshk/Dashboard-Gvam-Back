# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Si settings.db_port es None o 0, usar 5432 por defecto
db_port = settings.db_port or 5432

# URL de conexión a PostgreSQL
DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{db_port}/{settings.db_name}"
)

# Crea el engine con echo=True para ver las sentencias SQL en los logs,
# y future=True para compatibilidad con SQLAlchemy 2.0
engine = create_engine(DATABASE_URL, echo=True, future=True)

# sessionmaker para generar sesiones vinculadas al engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para los modelos ORM
Base = declarative_base()

def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    La sesión se cierra automáticamente al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
