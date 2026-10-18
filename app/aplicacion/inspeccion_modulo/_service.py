# app/aplicacion/inspeccion_modulo/_service.py

from app.aplicacion.inspeccion_modulo._repository import (
    Inspeccion_repository
)

class InspeccionService:

    async def obtener_suministro(
        self,
        db,
        headers: dict,
        payload: dict,
    ):
        return await Inspeccion_repository.obtener_suministro(
            db=db,
            headers=headers,
            payload=payload
        )



Inspeccion_service = InspeccionService()