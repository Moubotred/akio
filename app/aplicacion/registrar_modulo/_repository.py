from app.core.proxy import (
    Proxy_service
)

class RegistrarRepository:

    async def registrar_suministro(
        self,
        db,
        headers: dict,
        payload: dict
    ):
    
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/regis/suministro",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        if isinstance(response, list):
            # print("contenido: ",response)
            return response

        return response.json()

Registrar_repository = RegistrarRepository()