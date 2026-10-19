# app/aplicacion/configuracion_modulo/_service.py
from app.aplicacion.configuracion_modulo._repository import (
    configuracion_repository
)


class ConfiguracionService:

    async def obtener_configuracion_suministro(self, db, payload, headers):
        return await configuracion_repository.configuracion_suministro(
            db=db,
            headers=headers,
            payload=payload
        )

    async def obtener_configuracion_llave(self, db, payload, headers):
        return await configuracion_repository.configuracion_llave(
            db=db,
            headers=headers,
            payload=payload
        )

    async def obtener_configuracion_poste(self, db, payload, headers):
        return await configuracion_repository.configuracion_poste(
            db=db,
            headers=headers,
            payload=payload
        )

    async def obtener_configuracion_cajatoma(self, db, payload, headers):
        return await configuracion_repository.configuracion_cajatoma(
            db=db,
            headers=headers,
            payload=payload
        )

    async def validar_configuracion_foto(self, db, payload, headers):
        return await configuracion_repository.configuracion_foto(
            db=db,
            headers=headers,
            payload=payload
        )


Configuracion_service = ConfiguracionService()