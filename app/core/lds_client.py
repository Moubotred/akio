import httpx
from app.core.logger import get_logger
from asyncio import timeout
from app.core.constants import LDS

logger = get_logger("lds_client")

REMOVE_HEADERS = {
    "content-length",
    "transfer-encoding",
    "connection",
    "host",
    "x-forwarded-for",
    "x-forwarded-host",
    "x-forwarded-proto",
    "accept-encoding",
}

PAYLOAD_MOD = {
    "/ObtenerSSTMiPlanificacion": 
        {'parametroDto': 
            {
            'aplicacion': 'com.luzdelsur.proydist.sad', 
            'imei': '1aadd0f0b38ca460', 
            'porcentajeAvanceCero': False, 
            'tipoAtencion': 'SACATASTRO',
            'tokenFCM':""
        }
    },

    "/Obtener": ""
}


class LDSClient:

    def __init__(self):

        self.timeout = httpx.Timeout(
            connect=20,
            read=60,
            write=60,
            pool=60
        )

    def build_url(
        self,
        endpoint_key: str
    ) -> str:

        service_name, endpoint = (
            LDS.ENDPOINTS[endpoint_key]
        )

        service_path = (
            LDS.SERVICES[service_name]
        )

        return (
            f"{LDS.BASE_URL}/"
            f"{service_path}/"
            f"{endpoint}"
        )

    def apply_payload_mod(self,endpoint_key, payload):

        mods = PAYLOAD_MOD.get(endpoint_key)

        if not mods:
            return payload

        for path, value in mods.items():
            keys = path.split(".")
            current = payload

            for key in keys[:-1]:
                current = current.setdefault(key, {})

            current[keys[-1]] = value

        return payload

    def sanitize_headers(
        self,
        headers: dict
    ) -> dict:

        clean = {}

        for key, value in headers.items():

            if key.lower() in REMOVE_HEADERS:
                continue

            clean[key] = value

        return clean

    async def post(
        self,
        endpoint_key: str,
        payload: dict,
        headers: dict | None = None
    ):

        Url = self.build_url(
            endpoint_key
        )

        Payload = self.apply_payload_mod(endpoint_key,payload)

        clean_headers = (
            self.sanitize_headers(
                headers or {}
            )
        )

        logger.debug(f"[+] URL: {Url}")
        logger.debug(f"[+] PAYLOAD: {Payload}")
        logger.debug(f"[+] HEADERS: {clean_headers}")

        async with httpx.AsyncClient(verify=False,timeout=70) as client:

            response = await client.post(
                url=Url,
                json=Payload,
                headers=clean_headers
            )

            response.raise_for_status()

            return response

    async def post_binary(
        self,
        url: str,
        binary_data: bytes,
        headers: dict
    ):

        clean_headers = (
            self.sanitize_headers(
                headers
            )
        )

        async with httpx.AsyncClient(
            timeout=self.timeout,
            verify=False
        ) as client:

            response = await client.post(
                url=url,
                content=binary_data,
                headers=clean_headers
            )

            response.raise_for_status()


            return response

    async def post_with_auth(
        self,
        endpoint_key: str,
        jwt_token: str,
        payload: dict,
        headers: dict | None = None
    ):

        clean_headers = (
            self.sanitize_headers(
                headers or {}
            )
        )

        clean_headers[
            "authlds"
        ] = jwt_token

        return await self.post(
            endpoint_key=endpoint_key,
            payload=payload,
            headers=clean_headers
        )

    async def post_stream(
        self, 
        endpoint_key: str, 
        payload: dict, 
        headers: dict
    ):
        
        Url = self.build_url(endpoint_key)

        # Es fundamental usar un cliente asíncrono que soporte streaming
        async with httpx.AsyncClient(verify=False,timeout=70) as client:
            async with client.stream(
                "POST", 
                Url,
                json=payload, 
                headers=headers
            ) as response:
                # Transmitimos el cuerpo de la respuesta en bloques de 16 KB
                async for chunk in response.aiter_bytes(chunk_size=1024 * 16):
                    yield chunk

Lds_client = LDSClient()
