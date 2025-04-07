# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from init_admin import initialize_admin
from endpoints import auth_router, products_router, orders_router, repairs_router, receptions_router, reports_router

app = FastAPI(
    title="Gestión de Inventario y Autenticación API",
    description="API para autenticación y administración de productos, órdenes, reparaciones, recepciones e informes.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(products_router, prefix="/api/products")
app.include_router(orders_router, prefix="/api/orders")
app.include_router(repairs_router, prefix="/api/repairs")
app.include_router(receptions_router, prefix="/api/receptions")
app.include_router(reports_router, prefix="/api/reports")

@app.on_event("startup")
async def startup_event():
    initialize_admin()

@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
