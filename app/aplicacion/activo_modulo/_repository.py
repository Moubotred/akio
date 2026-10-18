from app.core.proxy import Proxy_service

class ActivoRepository:
    async def obtener_grado_corrocion(self,db,payload,headers):
    #    return await Proxy_service.post(db,"/gradocorrocion",payload,headers)
        response = await Proxy_service.post(
                db=db,
                endpoint_key="/poste/gradocorrosion",
                payload=payload,
                headers=headers
            )

        if isinstance(response, dict):
            return response

        return response.json() # type: ignore
        
