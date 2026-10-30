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

    async def obtener_tipofotos(
        self,
        db,
        headers: dict,
        payload: dict,
    ):
        return await Inspeccion_repository.obtener_tipofotos(
                    db=db,
                    headers=headers,
                    payload=payload
                )

    async def ob_registrar_suministro(
        self,
        db,
        headers: dict,
        payload: dict,
        ):
            return await Inspeccion_repository.ob_registrar_suministro(
                        db=db,
                        headers=headers,
                        payload=payload
                    )

Inspeccion_service = InspeccionService()