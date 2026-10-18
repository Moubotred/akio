# app/services/atencion_service.py
from app.aplicacion.atencion_modulo._repository import atencion_repository
from app.core.logger import get_logger

logger = get_logger("Atencion-service")

class AtencionService:
    

    async def obtener_tipo_atencion_capataz(
        self,
        db,
        payload,
        headers
    ):
         
        return await atencion_repository.obtener_tipo_atencion_capataz(
                db,
                payload,
                headers
            )
        

    # async def obtener_tipo_documento_por_atencion(
    #     self,
    #     payload,
    #     headers
    # ):

    #     return await atencion_repository.obtener_tipo_documento_por_atencion(
    #             payload,
    #             headers
    #         )
        

Atencion_service = AtencionService()