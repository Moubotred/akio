# app/aplicacion/mapa_modulo/mapa.py
from fastapi import APIRouter,Depends,Request,Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.lds_client import Lds_client
from app.core.database import get_db
from app.core.logger import get_logger
from app.aplicacion.mapa_modulo._service  import Mapa_service


router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc/mapa",
    tags=["Mapa"]
)

logger = get_logger("mapa")

@router.post("/paquetestrabajo")
async def obtener_paquetes_trabajo(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await Mapa_service.obtener_paquetes_trabajo(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

    logger.debug(f"[-] Trabajo: {data[0]["cantInsEnInspeccion"]}")
    
    return JSONResponse(data,200,headers_user)

@router.post("/paquetesinspeccion")
async def obtener_paquetes_inspeccion(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Mapa_service.obtener_paquetes_inspeccion(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

