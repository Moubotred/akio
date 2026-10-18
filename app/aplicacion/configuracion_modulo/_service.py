from app.aplicacion.configuracion_modulo._repository import (
    configuracion_repository
)


class ConfiguracionService:

    async def obtener_configuracion_suministro(self,db,payload,headers):
        pass

    async def obtener_configuracion_llave(self,db,payload,headers):
        pass

    async def obtener_configuracion_poste(self,db,payload,headers):
        pass

    async def obtener_configuracion_cajatoma(self,db,payload,headers):
        pass

    async def validar_configuracion_foto(self,db,payload,headers):
        pass
        

Configuracion_service = ConfiguracionService()