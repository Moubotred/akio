# app/aplicacion/configuracion_modulo/configuracion.py
from fastapi import APIRouter,Depends,Request,Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.aplicacion.configuracion_modulo._service import Configuracion_service

router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion",
    tags=["Configuracion"]
)

@router.post("/suministro")
async def obtener_conf_suministro(
    request:Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Configuracion_service.obtener_configuracion_suministro(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

@router.post("/llave")
async def obtener_conf_llave(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Configuracion_service.obtener_configuracion_llave(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

@router.post("/poste")
async def obtener_conf_poste(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Configuracion_service.obtener_configuracion_poste(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

@router.post("/cajatoma")
async def obtener_conf_cajatoma(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Configuracion_service.obtener_configuracion_cajatoma(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

@router.post("/valida/foto")
async def validar_conf_foto(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Configuracion_service.validar_configuracion_foto(
        db,
        payload=payload,
        headers=dict(request.headers)
    )