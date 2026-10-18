# app/repositorioes/capataz_repository.py

import json
from app.core.logger import get_logger
from app.core.proxy import (
    Proxy_service
)

logger = get_logger("capataz_repo")

class CapatazRepository:

    async def obtener_tipo_instancia_sad(
        self,
        db,
        headers: dict,
        payload: dict
    ):

        response = await Proxy_service.post(
            db=db,
            endpoint_key="/ObtenerTipoInstanciaSAD",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        return response.json() # type: ignore

    async def obtener_inicio_jornada(
        self,
        db,
        headers: dict,
        payload: dict
    ):

        response = await Proxy_service.post(
            db=db,
            endpoint_key="/IniciarJornada",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        return response.json() # type: ignore

    async def obtener_finalizacion_jornada(
        self,
        db,
        headers: dict,
        payload: dict
    ):

        response = await Proxy_service.post(
            db=db,
            endpoint_key="/FinalizarJornada",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        return response.json() # type: ignore

    async def obtener_sst_mi_planificacion_stream(self,
        db,
        headers: dict,
        payload: dict
    ):
        async for chunk in Proxy_service.post_stream(
            db=db,
            endpoint_key="/ObtenerSSTMiPlanificacion",
            payload=payload,
            headers=headers
        ):
            yield chunk

    async def obtener_sst_mi_planificacion(
        self,
        db,
        headers: dict,
        payload: dict
    ):

        response = await Proxy_service.post(
            db=db,
            endpoint_key="/ObtenerSSTMiPlanificacion",
            payload=payload,
            headers=headers
        )

        _keys_ = response.json()

        logger.debug(f"[+] Lista Items de SST {_keys_.keys()}") # type: ignore

        if isinstance(response, dict):
            return response

        return response.json() # type: ignore

    async def obtener_tipo_documento_por_atencion(
        self,
        db,
        headers: dict,
        payload: dict
    ):

        response = await Proxy_service.post(
            db=db,
            endpoint_key="/ObtenerTipoDocumentoPorAtencion",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        return response.json() # type: ignore
    

capataz_repository = CapatazRepository()