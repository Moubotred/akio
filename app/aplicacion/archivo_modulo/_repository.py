# app/repositories/atencion_repository.py

from app.services.proxy_service import (
    Proxy_service
)

class ArchivoRepository:

    async def obtener_tipo_doc_atencion(self,
        db,
        payload:dict,
        headers:dict
    ):

        return await Proxy_service.post(
            db,
            endpoint_key="/ObtenerTipoDocumentoPorAtencion",
            payload=payload,
            headers=headers
        )
    
    async def agregar_doc(self,
        db,
        payload:dict,
        headers:dict                  
    ):
        # aun por definir que se hace con la informacion
        
        pass


archivo_repository = ArchivoRepository()