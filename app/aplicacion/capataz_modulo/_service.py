from app.core.proxy import Proxy_service
from app.core.logger import get_logger
from app.aplicacion.capataz_modulo._repository import (
    capataz_repository
)

logger = get_logger("capataz_service")

class CapatazService:

    async def obtener_tipo_instancia_sad(
        self,
        db,
        headers: dict,
        payload: dict
    ):

        return await capataz_repository.obtener_tipo_instancia_sad(
            db=db,
            headers=headers,
            payload=payload
        )

    async def obtener_inicio_jornada(
            self,
            db,
            headers: dict,
            payload: dict
        ):

            return await capataz_repository.obtener_inicio_jornada(
                db=db,
                headers=headers,
                payload=payload
            )
    
    async def obtener_finalizacion_jornada(
            self,
            db,
            headers: dict,
            payload: dict
        ):

            return await capataz_repository.obtener_finalizacion_jornada(
                db=db,
                headers=headers,
                payload=payload
            )

    # 1. Canal de Streaming para usuario
    async def obtener_sst_mi_planificacion_stream(self,db,payload,headers):
        logger.debug("[-] Realizando peticion en Tiempo real")
        async for chunk in Proxy_service.post_stream(
            db=db,
            endpoint_key="/ObtenerSSTMiPlanificacion",
            payload=payload,
            headers=headers
        ):
            yield chunk
    
    # 2 Canal de peticion de proxy para gestionar la db
    async def obtener_sst_mi_planificacion_http(
        self,
        db,
        headers: dict,
        payload: dict
    ):
        # usar dto del app para el sst
        # referencias:
        #       https://gemini.google.com/app/f3da99fc9eb0490f
        return await capataz_repository.obtener_sst_mi_planificacion(
            db=db,
            headers=headers,
            payload=payload
        )

    async def obtener_tipo_documento_por_atencion(
        self,
        db,
        headers: dict,
        payload: dict
    ):

        return await capataz_repository.obtener_tipo_documento_por_atencion(
            db=db,
            headers=headers,
            payload=payload
        )
    
Capataz_service = CapatazService()