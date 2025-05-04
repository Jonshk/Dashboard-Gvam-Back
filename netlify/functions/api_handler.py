# netlify/functions/api_handler.py
from fastapi import FastAPI
from mangum import Mangum
from endpoints import auth, centers, orders, receptions, repairs, reports, stock

app = FastAPI()
# Incluye cada router con el prefijo /api
app.include_router(auth.router,      prefix="/api/auth")
app.include_router(centers.router,   prefix="/api/centers")
app.include_router(orders.router,    prefix="/api/orders")
app.include_router(receptions.router,prefix="/api/receptions")
app.include_router(repairs.router,   prefix="/api/repairs")
app.include_router(reports.router,   prefix="/api/reports")
app.include_router(stock.router,     prefix="/api/stock")

handler = Mangum(app)
