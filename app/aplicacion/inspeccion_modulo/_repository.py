from app.core.proxy import Proxy_service

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
    
    async def obtener_tipofotos(
            self,
            db,
            headers: dict,
            payload: dict
        ):
            response = await Proxy_service.post(
                db=db,
                endpoint_key="/tipofotos",
                payload=payload,
                headers=headers
            )
    
            if isinstance(response, dict):
                return response
    
            return response.json()

    async def ob_registrar_suministro(
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

        return response.json()

Inspeccion_repository = InspeccionRepository()