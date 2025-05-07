# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# configura y crea tablas…
from database import engine, Base, SessionLocal
from models import StockCategory, StockSubcategory

# importa tu script de admin
import init_admin

# importa routers…
from endpoints.auth       import auth_router
from endpoints.centers    import router as centers_router
from endpoints.orders     import router as orders_router
from endpoints.repairs    import repairs_router
from endpoints.receptions import receptions_router
from endpoints.stock      import stock_router

# —————— SEEDER ——————
def seed_stock_data():
    names = ["Repuestos", "Dispositivos", "Insumos"]
    db = SessionLocal()
    try:
        # 1) Crear categorías si no existen
        for name in names:
            if not db.query(StockCategory).filter_by(name=name).first():
                db.add(StockCategory(name=name))
        db.commit()

        # 2) Crear subcategorías espejo si no existen
        for cat in db.query(StockCategory).all():
            if not db.query(StockSubcategory)\
                     .filter_by(category_id=cat.id, name=cat.name)\
                     .first():
                db.add(StockSubcategory(category_id=cat.id, name=cat.name))
        db.commit()
    finally:
        db.close()


# —————— INICIALIZACIÓN ——————
# (¡OJO! Esto BORRA todas las tablas y datos existentes)
Base.metadata.drop_all(bind=engine)

# crea todas las tablas con la estructura actual de tus modelos
Base.metadata.create_all(bind=engine)

# si quieres correr el seeder **antes** de arrancar FastAPI:
seed_stock_data()


app = FastAPI(title="Inventario GVAM API")

# CORS…
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# registra routers
app.include_router(auth_router,       prefix="/auth",     tags=["auth"])
app.include_router(centers_router,    prefix="/centers",  tags=["centers"])
app.include_router(orders_router,     prefix="/orders",   tags=["orders"])
app.include_router(repairs_router,    prefix="/repairs",  tags=["repairs"])
app.include_router(receptions_router,prefix="/receptions",tags=["receptions"])
app.include_router(stock_router,      prefix="/stock",    tags=["stock"])

@app.on_event("startup")
def on_startup():
    # crea usuario admin si no existe
    init_admin.create_admin()

@app.get("/")
def read_root():
    return {"message": "API Inventario GVAM funcionando"}
