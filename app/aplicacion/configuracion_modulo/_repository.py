# app/aplicacion/configuracion_modulo/_repository.py
from app.core.proxy import Proxy_service


class ConfiguracionRepository:

    async def configuracion_suministro(
        self,
        db,
        headers: dict,
        payload: dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/conf/suministro",
            payload=payload,
            headers=headers
        )

        if isinstance(response, list):
            print("contenido: ", response)
            return response

        if isinstance(response, dict):
            return response

        return response.json()

    async def configuracion_llave(
        self,
        db,
        headers: dict,
        payload: dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/conf/llave",
            payload=payload,
            headers=headers
        )

        if isinstance(response, list):
            print("contenido: ", response)
            return response

        if isinstance(response, dict):
            return response

        return response.json()

    async def configuracion_poste(
        self,
        db,
        headers: dict,
        payload: dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/conf/poste",
            payload=payload,
            headers=headers
        )

        if isinstance(response, list):
            print("contenido: ", response)
            return response

        if isinstance(response, dict):
            return response

        return response.json()

    async def configuracion_cajatoma(
        self,
        db,
        headers: dict,
        payload: dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/conf/cajatoma",
            payload=payload,
            headers=headers
        )

        if isinstance(response, list):
            print("contenido: ", response)
            return response

        if isinstance(response, dict):
            return response

        return response.json()

    async def configuracion_foto(
        self,
        db,
        headers: dict,
        payload: dict
    ):
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/conf/valida/foto",
            payload=payload,
            headers=headers
        )

        if isinstance(response, list):
            print("contenido: ", response)
            return response

        if isinstance(response, dict):
            return response

        return response.json()


configuracion_repository = ConfiguracionRepository()