# app/core/proxy_service.py

import httpx

from app.core.logger import get_logger
from app.core.lds_client import Lds_client


logger = get_logger("proxy_service")

class ProxyService:

    async def post(
        self,
        db,
        endpoint_key: str,
        payload: dict,
        headers: dict
    ):

        response = await Lds_client.post(
            endpoint_key=endpoint_key,
            payload=payload,
            headers=headers
        )

        try:
            state_data = response
        except Exception as e:
            logger.warning(f"[-] La conexion fallo : {e}")
            state_data =  response

        return state_data
    
    # 1. Generador para Streaming
    async def post_stream(
        self,
        db,
        endpoint_key: str,
        payload: dict,
        headers: dict
    ):
        try:
            logger.debug("[-] Realizando peticion en Tiempo real con post stream")
            async for chunk in Lds_client.post_stream(
                endpoint_key=endpoint_key,
                payload=payload,
                headers=headers
            ):
                yield chunk
        except Exception as e:
            logger.warning(f"[-] Error en proxy streaming: {e}")
            raise e

Proxy_service = ProxyService()
