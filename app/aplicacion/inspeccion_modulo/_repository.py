from app.services.proxy_service import (
    Proxy_service
)

class InspeccionRepository:
    
    async def obtener_suministro(
        self,
        db,
        headers: dict,
        payload: dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/ObtenerTipoInstanciaSAD",
            payload=payload,
            headers=headers
        )

        if isinstance(response, dict):
            return response

        return response.json()


Inspeccion_repository = InspeccionRepository()