# app/services/auth_service.py

import json
import hashlib
from typing import Dict, Any
import asyncio

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from httpx import Response
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import LDS

from app.aplicacion.login_modulo._models import SolicitudDispositivo
from app.aplicacion.login_modulo._repository import auth_repository

from app.core.proxy import Proxy_service
from app.core.logger import get_logger
from app.core.exceptions import AppException

logger = get_logger("auth_service")

from fastapi import HTTPException
import json


class Tools:
    def hash_payload(self, data: SolicitudDispositivo) -> str:
        """Calcula un hash SHA-256 del modelo para comparar cambios."""
        data_dict = data.model_dump()
        data_string = json.dumps(data_dict, sort_keys=True, default=str)
        return hashlib.sha256(data_string.encode("utf-8")).hexdigest()

    async def verify_device_status(
        self,
        data: SolicitudDispositivo,
        redis: aioredis.Redis
    ):
        """Verifica el estado del dispositivo en los Sets de Redis."""
        device_id = data.credenciales.idDispositivo

        if not device_id:
            raise HTTPException(
                status_code=400, 
                detail="idDispositivo no especificado"
            )

        # 1. Verificar si el dispositivo está bloqueado
        if await redis.sismember(LDS.REDIS_BLOCKED_SETS, device_id):
            logger.info("[+] revision de bloqueo")
            raise AppException(
                "DISPOSITIVO BLOQUEADO "    \
                "EN EL SISTEMA NO ESTAS "   \
                "SUSCRITO AL PROXY "    \
                "CONTACTAR POR WHATSAPP " \
                "CON EL BOT @kimshizi " \
                "USANDO EL COMANDO\n\n" \
                
                "* /start \n\t\tpara iniciar " \
                "el proceso de registro \n\n"

                # "* /panel \n\t\tpara adquirir " \
                # "mas servicios\n\n"

                # "* /suport \n\t\tpara contactar " \
                # "a soporte tecnico \n\n"

                # "* /panel \n\t\tpara adquirir " \
                # "mas servicios\n\n"
            )
            # raise AppException("Dispositivo bloqueado en el sistema no estas suscrito al proxy")

            # return JSONResponse(status_code = 400, content="Dispositivo bloqueado en el sistema")
        
            # raise HTTPException(
            #     status_code=403, 
            #     detail="Dispositivo bloqueado en el sistema"
            # )
            

        # 2. Verificar si está pre-aprobado
        if await redis.sismember(LDS.REDIS_APPROVED_SETS, device_id):
            return {
                "estado": "OK", 
                "mensaje": "Dispositivo pre-aprobado"
            }
        
        return None  # Estado PENDING (Requiere autorización)

    async def notify_frontend_new_request(
        self, 
        redis: aioredis.Redis, 
        payload_notification: Dict[str, Any]
    ) -> None:
        """Publica la nueva solicitud en el canal global de notificaciones para el frontend."""
        payload_str = json.dumps(payload_notification, default=str)
        # Canal unificado para la interfaz de administración
        await redis.publish("channel:approval:global", payload_str)
        logger.info(
            f"[+] Notificación enviada al canal global para el dispositivo {payload_notification.get('device_id')}"
        )

    async def wait_for_device_approval(
        self,
        device_id: str,
        redis: aioredis.Redis,
        timeout: int = 30
    ) -> bool:
        """Suscripción al canal específico del dispositivo a la espera del veredicto del Admin."""
        pubsub = redis.pubsub()
        channel_name = f"channel:device:{device_id}"
        
        await pubsub.subscribe(channel_name)
        logger.info(f"[*] Suscrito al canal de aprobación: {channel_name}")

        start_time = asyncio.get_event_loop().time()
        try:
            while (asyncio.get_event_loop().time() - start_time) < timeout:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, 
                    timeout=1.0
                )
                if message and message.get("data"):
                    raw_data = message["data"]
                    if isinstance(raw_data, bytes):
                        raw_data = raw_data.decode("utf-8")
                    data = json.loads(raw_data)
                    
                    if data.get("status") in ["approved", "APPROVED"]:
                        return True
                    elif data.get("status") in ["blocked", "BLOCKED"]:
                        return False
                await asyncio.sleep(0.5)
            return False
        finally:
            await pubsub.unsubscribe(channel_name)
            await pubsub.close()

    async def authorization_device(
        self,
        data: SolicitudDispositivo,
        redis: aioredis.Redis
    ) -> None:
        """Valida estado en Redis y si está pendiente inicia la espera."""
        status = await self.verify_device_status(data, redis)
        
        if status and status.get("estado") == "OK":
            return

        device_id = data.credenciales.idDispositivo
        
        notification_payload = {
            "device_id": device_id,
            "username": getattr(data.credenciales, "usuario", None),
            "empresa": getattr(data.credenciales, "empresa", None),
            "version_android": getattr(data.credenciales, "versionAndroid", None),
        }
        
        # 1. Emitir evento hacia el Dashboard Frontend
        await self.notify_frontend_new_request(redis, notification_payload)

        # 2. Bloquear la petición de la APK hasta recibir respuesta por PubSub
        approved = await self.wait_for_device_approval(device_id, redis, timeout=30)
        if not approved:
            raise AppException(
                "NO ESTAS AUTORIZADO "  \
                "POR KIMSHIZI PARA USAR  " \
                "ESTE SERVICIO "      \
                "CONTACTAR POR WHATSAPP " \
                "CON EL BOT @kimshizi "   \
                "USANDO EL COMANDO\n\n"   \
                "\n* /suport \n\t\tpara contactar " \
                "a soporte tecnico \n\n"

                      )
        
            # raise HTTPException(
            #     status_code=408, 
            #     detail="No estas autorizado por kimshizi para el servicio"
            # )

    async def check_database_payload(
        self,
        db: AsyncSession,
        data: SolicitudDispositivo
    ) -> None:
        hash_data = self.hash_payload(data)

        if await auth_repository.verify_payload_hash(db, hash_data):
            logger.info("[-] Payload ya registrado previamente")
        else:
            await auth_repository.save_request_user(
                db=db,
                data=data,
                hash=hash_data
            )
            logger.info("[+] Nuevo payload registrado en BD")


class AuthService(Tools):

    async def validar_credenciales(
        self,
        db: AsyncSession,
        redis: aioredis.Redis,
        data: SolicitudDispositivo,
        headers: dict
    ):
        # 1. Registrar payload en base de datos
        await self.check_database_payload(db, data)
        
        # 2. Verificar autorización del dispositivo en Redis
        await self.authorization_device(data, redis)
        
        # 3. Respuesta en caso de éxito
        response = await Proxy_service.post(
            db=db,
            endpoint_key="/ValidaCredenciales",
            payload=data.model_dump(),
            headers=headers
        )

        try:
            data_reponse = response.json() # type: ignore

            # logger.debug(f"[-] contenido : {response.content} ") # type: ignore
            if response.status_code != 200: # type: ignore
                logger.debug("[-] Fallo en validacion ")
                raise HTTPException(401,detail="usuario no validado")
            
            # logger.debug(f"[+] Tipo: {type(response)}")     
            await auth_repository.save_reponse_user(
                db=db,
                data=data_reponse
            )
            return 200,data_reponse # type: ignore
        
        except Exception as e:
            logger.warning(f"[x] sucedio un error: {e}")
            return 500,f"{e}"
        

Auth_service = AuthService()


        # hash_data = await self.hashear_payload(data)

        # if await auth_repository.verify_payload_hash(db,hash_data):
        #     logger.info("[-] Payload ya registrado con anterioridad")

        # else:

        #     await auth_repository.save_request_user(
        #             db=db,
        #             data=data,
        #             hash = hash_data
        #     )

            # logger.info("[+] Payload nuevo registrado")
            # await self.authorization_device(data)

        # response = await Proxy_service.post(
        #     db=db,
        #     endpoint_key="/ValidaCredenciales",
        #     payload=data,
        #     headers=headers
        # )

        # try:
        #     data_reponse = response.json() # type: ignore

        #     # logger.debug(f"[-] contenido : {response.content} ") # type: ignore
        #     if response.status_code != 200: # type: ignore
        #         logger.debug("[-] Fallo en validacion ")
        #         raise HTTPException(401,detail="usuario no validado")
            
        #     # logger.debug(f"[+] Tipo: {type(response)}")     
        #     await auth_repository.save_reponse_user(
        #         db=db,
        #         data=data_reponse
        #     )
        #     return 200,data_reponse # type: ignore
        
        # except Exception as e:
        #     return 500,f"{e}"


    

    # async def sessions(self,db:AsyncSession,_data_: dict):

    #     try:
    #         # 1. Crear instancia raíz
    #         respuesta = SessionResponse(
    #             token=_data_["token"],
    #             disco_servidor_log=_data_.get("discoServidorLog"),
    #             path_servidor_log=_data_.get("pathServidorLog"),
    #             dias_restantes_caducar_clave=_data_.get("diasRestantesParaCaducarClave"),
    #             info_plataforma=_data_.get("infoPlataforma"),
    #             rastrea_equipo=_data_.get("rastreaEquipo", False),
    #             tiempo_rastreo=_data_.get("tiempoRastreo"),
    #             requiere_mfa=_data_.get("requiereMFA", False),
                
    #             # Lista 1:N de Aplicaciones
    #             aplicaciones=[
    #                 Application(
    #                     paquete=app["paquete"],
    #                     nombre=app["nombre"],
    #                     version=app["version"],
    #                     obligatorio=app["obligatorio"],
    #                     id_plugin=str(app["idPlugin"]),
    #                     es_favorito=app["esFavorito"],
    #                     es_visible=app["esVisible"],
    #                     url=app.get("url")
    #                 ) for app in _data_.get("aplicaciones", [])
    #             ],
                
    #             # Objeto 1:1 Sesión de Servicio
    #             sesion_servicio=ServiceSession(
    #                 id_sesion=_data_["sesionServicio"]["idSesion"],
    #                 id_dispositivo=_data_["sesionServicio"]["idDispositivo"],
    #                 token_id=_data_["sesionServicio"]["tokenId"],
    #                 ip_cliente=_data_["sesionServicio"]["ipCliente"],
    #                 usuario_host=_data_["sesionServicio"].get("usuarioHost"),
    #                 token_sesion=_data_["sesionServicio"].get("TokenSesion"),
                    
    #                 # Sub-Objeto 1:1 Usuario
    #                 usuario=SessionUser(
    #                     nombre=_data_["sesionServicio"]["usuario"]["nombre"],
    #                     ficha=_data_["sesionServicio"]["usuario"].get("ficha"),
    #                     cr=_data_["sesionServicio"]["usuario"].get("cr"),
    #                     email=_data_["sesionServicio"]["usuario"]["email"],
    #                     id_empresa_logeo=_data_["sesionServicio"]["usuario"]["idEmpresaLogeo"],
    #                     id_empresa_trabaja=_data_["sesionServicio"]["usuario"]["idEmpresaTrabaja"],
    #                     usuario_logeo=_data_["sesionServicio"]["usuario"]["usuarioLogeo"],
    #                     rol=",".join(_data_["sesionServicio"]["usuario"].get("rol", []))
    #                 ),
                    
    #                 # Lista 1:N Accesos a BD
    #                 accesos_bd=[
    #                     DatabaseAccess(
    #                         tag=acc["Tag"],
    #                         escritura=acc["Escritura"],
    #                         lectura=acc["Lectura"]
    #                     ) for acc in _data_["sesionServicio"].get("accesoBD", [])
    #                 ]
    #             )
    #         )

    #         # 2. Guardar en Cascada
    #         db.add(respuesta)
    #         await db.commit()
    #         await db.refresh(respuesta)
    #         return respuesta

    #     except Exception as e:
    #         await db.rollback()
    #         raise e
        
    #     finally:
    #         await db.close()

    # async def terminate(
    #     self,
    #     db: AsyncSession,
    #     token: str
    # ):

    #     stmt = select(Session).where(
    #         Session.jwt_token == token,
    #         Session.is_active == True
    #     )

    #     result = await db.execute(stmt)

    #     session = result.scalar_one_or_none()

    #     if not session:
    #         return

    #     session.is_active = False
    #     session.last_activity = datetime.utcnow()

    #     await db.commit()

    # async def _create_or_update_user(
    #     self,
    #     db: AsyncSession,
    #     lds_response: dict
    # ) -> User:

    #     sesion = lds_response.get(
    #         "sesionServicio",
    #         {}
    #     )

    #     usuario = sesion.get(
    #         "usuario",
    #         {}
    #     )

    #     username = usuario.get(
    #         "usuarioLogeo"
    #     )

    #     stmt = select(User).where(
    #         User.username == username
    #     )

    #     result = await db.execute(stmt)

    #     user = result.scalar_one_or_none()

    #     if user:

    #         user.nombre = usuario.get("nombre")
    #         user.email = usuario.get("email")
    #         user.empresa_logeo = usuario.get(
    #             "idEmpresaLogeo"
    #         )
    #         user.empresa_trabaja = usuario.get(
    #             "idEmpresaTrabaja"
    #         )
    #         user.rol = ",".join(
    #             usuario.get("rol", [])
    #         )
    #         user.last_login = datetime.utcnow()

    #         await db.commit()

    #         return user

    #     user = User(
    #         username=username,
    #         nombre=usuario.get("nombre"),
    #         email=usuario.get("email"),
    #         empresa_logeo=usuario.get(
    #             "idEmpresaLogeo"
    #         ),
    #         empresa_trabaja=usuario.get(
    #             "idEmpresaTrabaja"
    #         ),
    #         rol=",".join(
    #             usuario.get("rol", [])
    #         ),
    #         last_login=datetime.utcnow()
    #     )

    #     db.add(user)

    #     await db.commit()

    #     await db.refresh(user)

    #     return user

    # async def _create_session(
    #     self,
    #     db: AsyncSession,
    #     user: User,
    #     payload: dict,
    #     lds_response: dict
    # ):

    #     credenciales = payload.get(
    #         "credenciales",
    #         {}
    #     )

    #     device_id = credenciales.get(
    #         "idDispositivo"
    #     )

    #     sesion = lds_response.get(
    #         "sesionServicio",
    #         {}
    #     )

    #     jwt_token = lds_response.get(
    #         "token"
    #     )

    #     session = Session(
    #         user_id=user.id,
    #         device_id=device_id,
    #         jwt_token=jwt_token,
    #         lds_session_id=sesion.get(
    #             "idSesion"
    #         ),
    #         token_id=sesion.get(
    #             "tokenId"
    #         ),
    #         ip=sesion.get(
    #             "ipCliente"
    #         ),
    #         is_active=True
    #     )

    #     db.add(session)

    #     await db.commit()

    # async def _register_login_attempt(
    #     self,
    #     db: AsyncSession,
    #     payload: dict,
    #     success: bool,
    #     message: str
    # ):

    #     credenciales = payload.get(
    #         "credenciales",
    #         {}
    #     )

    #     attempt = LoginAttempt(
    #         username=credenciales.get(
    #             "usuario"
    #         ),
    #         device_id=credenciales.get(
    #             "idDispositivo"
    #         ),
    #         success=success,
    #         message=message
    #     )

    #     db.add(attempt)

    #     await db.commit()


Auth_service = AuthService()