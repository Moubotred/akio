# app/backend/auth.py

from fastapi.responses import JSONResponse,Response
from fastapi import APIRouter,Request,Depends,HTTPException

from httpx import request
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from app.core.database import get_db,get_redis
from app.aplicacion.login_modulo._models import SolicitudDispositivo,SolicitudParametros,DynamicPayload,TerminarPayload
from app.aplicacion.login_modulo._service import Auth_service
from app.core.lds_client import Lds_client

from app.core.logger import get_logger

router = APIRouter(
    prefix="/interno/platafadr/framework/lanzador/PltAndroid.svc/Login",
    tags=["auth"]
)

logger = get_logger("auth")

@router.post("/ValidaCredenciales")
async def valida_credenciales(
    request:Request, 
    payload:SolicitudDispositivo, 
    db:AsyncSession = Depends(get_db),
    redis:aioredis.Redis = Depends(get_redis)
    ):

    status, response = await Auth_service.validar_credenciales(
        db = db,
        redis = redis,
        data = payload,
        headers = dict(request.headers)
        )

    return JSONResponse(status_code = status, content=response)

@router.post("/ParametrosIniciales")
async def parametros_iniciales(request:Request, payload:SolicitudParametros):
    # AGREGAR UN TRY EXCEPTION EN CASO DE QUE EL SERVIDOR FINAL NO ESTE DISPONIBLE 
    response = await Lds_client.post("/ParametrosIniciales",payload.model_dump(),dict(request.headers))
    return JSONResponse(response.json())

@router.post("/RegistroEjecucionAplicacion")
async def registro_ejecucion_aplicacion(request:Request,payload: DynamicPayload):
    logger.info(f"[-] payload indefinido esctructura: {payload}")

@router.post("/ValidarSesionActivaImei")
async def ValidarSesionActivaImei(request:Request,payload: DynamicPayload):
    logger.info(f"[-] payload indefinido esctructura: {payload}")


@router.post("/ObtieneVersionDisponible")
async def ObtieneVersionDisponible(request:Request):
    dat = await request.body()
    logger.info(f"datos de actulizacion: {dat}")

@router.post("/ActualizarEstadoGPSDispositivo")
async def ActualizarEstadoGPSDispositivo(request:Request):
    dat = await request.body()
    logger.info(f"coordendas de dispositivo: {dat}")

@router.post("/RegistrarUbicacion")
async def RegistrarUbicacion(request:Request):
    dat = await request.body()
    logger.info(f"registro ubicacion: {dat}")    
# @router.post("/terminar")
# async def terminar(payload: TerminarPayload,db: AsyncSession = Depends(get_db)):

#     token_data = payload.token
#     jwt_token = token_data.get("Token")
#     if jwt_token:

#         await Auth_service.terminate(db=db,token=jwt_token)

#     return {
#         "success": True
#     }
