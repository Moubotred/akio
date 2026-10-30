# app/aplicacion/configuracion_modulo/configuracion.py
from fastapi import APIRouter,Depends,Request,Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import get_logger
from app.core.database import get_db
from app.core.lds_client import Lds_client
from app.aplicacion.configuracion_modulo._service import Configuracion_service

router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion",
    tags=["Configuracion"]
)

logger = get_logger("configuracion")

@router.post("/suministro")
async def obtener_conf_suministro(
    request:Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await Configuracion_service.obtener_configuracion_suministro(
        db,
        payload=payload,
        headers=headers_server
    )

    logger.debug(f"[+] SUMINITRO: {data[0]["descripcion"]}")

    return JSONResponse(data,200,headers_user)

@router.post("/llave")
async def obtener_conf_llave(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await Configuracion_service.obtener_configuracion_llave(
        db,
        payload=payload,
        headers=headers_server
    )
    return JSONResponse(data,200,headers_user)

@router.post("/poste")
async def obtener_conf_poste(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await Configuracion_service.obtener_configuracion_poste(
        db,
        payload=payload,
        headers=headers_server
    )

    logger.debug(f"[-] Poste {data[0]["descripcion"]}")

    return JSONResponse(data,200,headers_user)

@router.post("/cajatoma")
async def obtener_conf_cajatoma(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):

    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await Configuracion_service.obtener_configuracion_cajatoma(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

    logger.debug(f"[-] CAJA-TOMA: {data[0]["descripcion"]}")
    return JSONResponse(data,200,headers_user)

@router.post("/valida/foto")
async def validar_conf_foto(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await Configuracion_service.validar_configuracion_foto(
        db,
        payload=payload,
        headers=dict(request.headers)
    )
    logger.debug(f"[-] TIPO DE FOTO: {data[0]}")
    return JSONResponse(data,200,headers_user)