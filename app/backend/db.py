# app/backend/consultas.py

from fastapi import APIRouter,Depends
from fastapi import Form,Response,HTTPException,status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


import asyncio
import redis.asyncio as aioredis
from fastapi import Request
from sse_starlette.sse import EventSourceResponse
from app.core.database import get_redis


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.aplicacion.login_modulo._schema import Credential

from app.core.logger import get_logger

logger = get_logger("database")

database = APIRouter(
    prefix="/database",
    tags=["base de datos"]
)

@database.post("/consulta")
async def get_dashboard_data(db: AsyncSession = Depends(get_db)):
    query_cred = select(Credential)
    res_cred = await db.execute(query_cred)
    credencial = res_cred.scalars().first()

    print(credencial.id) # type: ignore
    print(credencial.usuario) # type: ignore
    print(credencial.password) # type: ignore
    print(credencial.dominio) # type: ignore
    print(credencial.empresa) # type: ignore

    print(credencial.empresa) # type: ignore
    print(credencial.empresa_contratante) # type: ignore
    print(credencial.id_dispositivo) # type: ignore
    print(credencial.version_android) # type: ignore
    # print(credencial.) # type: ignore




    # pass
    # try:
    #     # Consultar la tabla de credenciales
    #     query_cred = select(Credential)
    #     res_cred = await db.execute(query_cred)
    #     credencial = res_cred.scalars().first()

    #     # Extraer atributos con fallback en caso de tabla vacía
    #     id_val = credencial.id if credencial else 1
    #     user_val = credencial.usuario if credencial else "TGUISADO"
    #     domain_val = credencial.dominio if credencial else "EXTERNOSLDS.COM"
    #     # Si tu modelo Credential tiene la columna version, úsala; de lo contrario pon un valor por defecto
    #     version_val = getattr(credencial, "version", "3.2.2") if credencial else "3.2.2"

    #     return {
    #         "sesionServicio": {
    #             "idSesion": id_val,
    #             "usuario": {
    #                 "nombre": user_val,
    #                 "usuarioLogeo": user_val
    #             },
    #             "accesoBD": [
    #                 {"Lectura": True},
    #                 {"Lectura": True}
    #             ]
    #         },
    #         "diasRestantesParaCaducarClave": 13,
    #         "aplicaciones": [
    #             {
    #                 "idPlugin": id_val,
    #                 "nombre": domain_val,
    #                 "paquete": "com.lds.app",
    #                 "version": version_val,  # <-- Campo requerido por la tabla JS
    #                 "obligatorio": True,
    #                 "esVisible": True
    #             }
    #         ]
    #     }

    # except Exception as e:
    #     logger.debug(f"[-] Error: {e} ")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Error consultando la base de datos: {str(e)}"
    #     )


