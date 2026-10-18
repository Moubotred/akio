# app/core/tasks.py

import httpx

from app.core.logger import get_logger
from app.core.database import get_db_ctx
from app.core.lds_client import Lds_client

from app.aplicacion.capataz_modulo._service import Capataz_service

logger = get_logger("tasks")

# Gestiona la conexion en segundo plano para la usar 
# datos que responde el servidor 
# 
# * permite que el endpoint desde donde se llama a esta funcion
#   no se detenga y responda datos en tiempo real mediante 
#   StreamingResponse
# 
# * permite poder usar los datos del servidor en gestionar
#   datos a nivel de proxy

async def bd_background_sst(db,payload, headers):
    async with get_db_ctx() as db_session:
        try:
            await Capataz_service.obtener_sst_mi_planificacion_http(
                db=db_session,
                headers=headers,
                payload=payload
            )
        except Exception as e:
            logger.error(f"[-] Error en guardado en segundo plano: {e}")
