from app.core.proxy import Proxy_service


class ConfiguracionRepository:
    async def obtener_configuracion_suministro(self,
        db,
        headers:dict,
        payload:dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/conf/suministro",
            payload=payload,
            headers=headers
        )

        # print('conf: ',response)

        if isinstance(response, list):
            print("contenido: ",response)
            return response


        if isinstance(response, dict):
            return response

        
        return response.json()



configuracion_repository = ConfiguracionRepository()