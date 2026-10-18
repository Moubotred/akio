# app/repositories/atencion_repository.py

from app.core.proxy import (
    Proxy_service
)

from app.core.logger import get_logger

logger = get_logger("Atencion-repo")

class AtencionRepository:

    async def obtener_tipo_atencion_capataz(
        self,
        db,
        payload,
        headers
    ):
        

        response =  await Proxy_service.post(
            db,
            endpoint_key="/ObtenerTipoAtencionCapataz",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        return response.json() 

    # async def obtener_tipo_documento_por_atencion(
    #     self,
    #     payload,
    #     headers
    # ):

    #     return await Proxy_service.post(
    #         endpoint="/ObtenerTipoDocumentoPorAtencion",
    #         payload=payload,
    #         headers=headers
    #     )

atencion_repository = AtencionRepository()