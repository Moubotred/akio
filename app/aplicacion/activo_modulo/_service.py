from app.aplicacion.activo_modulo._repository import Activo_repository

class Activo_service:
    async def obtener_grado_corrocion(self,db,headers,payload):
        return await Activo_repository.obtener_grado_corrocion(db,payload,headers)

activo_service = Activo_service()