from fastapi import APIRouter,Request,Body,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.aplicacion.activo_modulo._service import activo_service
from app.core.database import get_db


router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc/activo",
    tags=["Activo"]
)

@router.post("/poste/gradocorrosion")
async def obtener_grado_corrocion(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    pass