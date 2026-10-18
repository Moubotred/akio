# app/routers/atencion.py


import json
from fastapi import APIRouter, Request, Depends,Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.aplicacion.atencion_modulo._service import Atencion_service
from app.core.logger import get_logger

router = APIRouter(
    prefix="/tecnicoi/spo/sad/atencion/Atencion.svc/Atencion",
    tags=["Atencion"]
)

logger = get_logger("atencion")

@router.post("/ObtenerTipoAtencionCapataz")
async def obtener_tipo_atencion_capataz(
    request: Request,
    payload: dict = Body(default={}),
    db: AsyncSession = Depends(get_db)

):  
    
    logger.info("[-] Atencion: test")

    return await Atencion_service.obtener_tipo_atencion_capataz(
        db,
        payload=payload,
        headers=dict(request.headers)
    )


# @router.post("/ObtenerTipoDocumentoPorAtencion")
# async def obtener_tipo_documento_por_atencion(
#     request: Request
# ):

#     payload = await request.json()

#     return await Atencion_service.obtener_tipo_documento_por_atencion(
#         payload=payload,
#         headers=dict(request.headers)
#     )