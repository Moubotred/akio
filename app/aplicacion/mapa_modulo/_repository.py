from app.core.proxy import (
    Proxy_service
)


class MapaRespository:
    
    async def obtener_paquetes_trabajo(self,
        db,
        headers:dict,
        payload:dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/paquetestrabajo",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        if isinstance(response, list):
            # print("contenido: ",response)
            return response

        return response.json()
    
    async def obtener_paquetes_inspeccion(self,
        db,
        headers:dict,
        payload:dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/paquetesinspeccion",
            payload=payload,
            headers=headers
        )
        
        print(type(response))

        if isinstance(response, dict):
            return response

        if isinstance(response, list):
            return response 

        return response.json()


Mapa_repository = MapaRespository()
