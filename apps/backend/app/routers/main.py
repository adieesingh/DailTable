import sys
from pathlib import Path

# Ensure backend root is on sys.path for reliable imports when running from subdirectories
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from app.routers.restaurant import router as restaurant_router
from app.routers.table import router as table_router
from app.routers.booking import router as booking_router

app = FastAPI(
    title="DailTable API",
    description="API for managing restaurants, tables, and reservations",
    version="0.1.0",
)

app.include_router(restaurant_router)
app.include_router(table_router)
app.include_router(booking_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to DailTable API",
        "docs": "/docs",
        "endpoints": [
            "/restaurants",
            "/tables",
            "/bookings",
        ],
    }