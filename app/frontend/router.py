from fastapi import APIRouter
from app.frontend.home_page import router as home_router
from app.frontend.dashboard_page import router as dashboard_router

frontend_router = APIRouter()

# Anidamos las subrutas del frontend
frontend_router.include_router(home_router)
frontend_router.include_router(dashboard_router)