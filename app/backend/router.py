from fastapi import APIRouter
from app.backend.db import database
from app.backend.sse import Event

backend = APIRouter(prefix="/api/v1",tags=["backend"])

# Anidamos los subrouters
# backend.include_router(database)
backend.include_router(Event)

