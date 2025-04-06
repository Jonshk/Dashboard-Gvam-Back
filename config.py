# config.py

import os

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),  # Usar el nombre del servicio en Docker por defecto
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "user": os.getenv("POSTGRES_USER", "gvam"),
    "password": os.getenv("POSTGRES_PASSWORD", "GVAM"),
    "database": os.getenv("POSTGRES_DB", "inventariogvam")
}

JWT_SECRET = "your_jwt_secret_key"  # Cambia esto por una clave segura en producción
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # 1 hora de validez

def get_database_url():
    """
    Construye la URL de conexión para SQLAlchemy.
    """
    return (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

# Definición de la variable DATABASE_URL para que otros módulos la importen
DATABASE_URL = "postgresql://gvam:GVAM@postgres:5432/inventariogvam?client_encoding=UTF8"

# Bloque de prueba: Imprime la DSN y prueba la conexión a la base de datos.
if __name__ == "__main__":
    from sqlalchemy import create_engine, text

    print("DSN:", repr(DATABASE_URL))
    
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
            print("Conexión establecida, resultado de prueba:", result)
    except Exception as e:
        print("Error al conectar:", e)
