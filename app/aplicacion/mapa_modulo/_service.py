from app.aplicacion.mapa_modulo._repository import (
    Mapa_repository
)

class MapaService:
    
    async def obtener_paquetes_trabajo(
            self,
            db,
            headers:dict,
            payload:dict
        ):

        return await Mapa_repository.obtener_paquetes_trabajo(
            db=db,
            headers=headers,
            payload=payload
        )
    
    async def obtener_paquetes_inspeccion(
            self,
            db,
            headers:dict,
            payload:dict
        ):

        return await Mapa_repository.obtener_paquetes_inspeccion(
            db=db,
            headers=headers,
            payload=payload
        )

Mapa_service = MapaService()