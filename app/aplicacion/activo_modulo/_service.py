from app.aplicacion.activo_modulo._repository import ActivoRepository

class Activo_service:
    async def obtener_grado_corrocion(self,db,headers,payload):
        return await ActivoRepository.obtener_grado_corrocion(db,headers,payload) # type: ignore


activo_service = Activo_service()