from app.aplicacion.registrar_modulo._repository import (
    Registrar_repository
)

class RegistrarService:

    async def registrar_suministro(self,
        db,
        headers: dict,
        payload: dict
    ):
        return await Registrar_repository.registrar_suministro(
            db=db,
            headers=headers,
            payload=payload
        )
    
Registrar_service = RegistrarService()