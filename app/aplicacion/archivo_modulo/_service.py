# app/services/archivo_service.py
from app.repositories.archivo_repository import (
    archivo_repository
)

class ArchivoService:
    async def obtener_tipo_doc_atencion(self,
        db,
        payload:dict,
        headers:dict
    ):
        return await archivo_repository.obtener_tipo_doc_atencion(
            db,
            payload,
            headers
        )
    
    async def agregar_doc(self,
        db,
        payload:dict,
        headers:dict
    ):
        return await archivo_repository.agregar_doc(
            db,
            payload,
            headers
        )




Archivo_service = ArchivoService()
