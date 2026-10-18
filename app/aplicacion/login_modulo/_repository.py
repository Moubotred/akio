from datetime import datetime, timezone
from sqlalchemy import select,exists
from sqlalchemy.ext.asyncio import AsyncSession


from app.aplicacion.login_modulo._schema import (
    Login,
    Credential,
    InstalledApp,
    Application,
    SessionResponse,
    ServiceSession,
    DatabaseAccess,
    SessionUser
)

class Auth_repository:

    async def save_request_user(self,db,data,hash):

        # verificar si el payload hash se ecuentra 
        # en la base de datos

        registro_cred = data.credenciales

        registro_login = Login(
            hash=hash,
            credenciales=Credential(
                usuario=registro_cred.usuario,
                password=registro_cred.password,
                dominio=registro_cred.dominio,
                empresa=registro_cred.empresa.strip(),
                empresa_contratante=registro_cred.empresaContratante.strip(),
                id_dispositivo=registro_cred.idDispositivo,
                version_android=registro_cred.versionAndroid,
                version_plataforma=registro_cred.versionPlataforma
            ),
            aplicaciones_instaladas=[
                InstalledApp(paquete=app.paquete, version=app.version)
                for app in data.aplicacionesInstaladas
            ]
        )
        
        db.add(registro_login)
        await db.commit()

    async def save_reponse_user(self,db,data):
        try:
            # 1. Crear instancia raíz
            respuesta = SessionResponse(
                token=data["token"],
                disco_servidor_log=data.get("discoServidorLog"),
                path_servidor_log=data.get("pathServidorLog"),
                dias_restantes_caducar_clave=data.get("diasRestantesParaCaducarClave"),
                info_plataforma=data.get("infoPlataforma"),
                rastrea_equipo=data.get("rastreaEquipo", False),
                tiempo_rastreo=data.get("tiempoRastreo"),
                requiere_mfa=data.get("requiereMFA", False),
                
                # Lista 1:N de Aplicaciones
                aplicaciones=[
                    Application(
                        paquete=app["paquete"],
                        nombre=app["nombre"],
                        version=app["version"],
                        obligatorio=app["obligatorio"],
                        id_plugin=str(app["idPlugin"]),
                        es_favorito=app["esFavorito"],
                        es_visible=app["esVisible"],
                        url=app.get("url")
                    ) for app in data.get("aplicaciones", [])
                ],
                
                # Objeto 1:1 Sesión de Servicio
                sesion_servicio=ServiceSession(
                    id_sesion=data["sesionServicio"]["idSesion"],
                    id_dispositivo=data["sesionServicio"]["idDispositivo"],
                    token_id=data["sesionServicio"]["tokenId"],
                    ip_cliente=data["sesionServicio"]["ipCliente"],
                    usuario_host=data["sesionServicio"].get("usuarioHost"),
                    token_sesion=data["sesionServicio"].get("TokenSesion"),
                    
                    # Sub-Objeto 1:1 Usuario
                    usuario=SessionUser(
                        nombre=data["sesionServicio"]["usuario"]["nombre"],
                        ficha=data["sesionServicio"]["usuario"].get("ficha"),
                        cr=data["sesionServicio"]["usuario"].get("cr"),
                        email=data["sesionServicio"]["usuario"]["email"],
                        id_empresa_logeo=data["sesionServicio"]["usuario"]["idEmpresaLogeo"],
                        id_empresa_trabaja=data["sesionServicio"]["usuario"]["idEmpresaTrabaja"],
                        usuario_logeo=data["sesionServicio"]["usuario"]["usuarioLogeo"],
                        rol=",".join(data["sesionServicio"]["usuario"].get("rol", []))
                    ),
                    
                    # Lista 1:N Accesos a BD
                    accesos_bd=[
                        DatabaseAccess(
                            tag=acc["Tag"],
                            escritura=acc["Escritura"],
                            lectura=acc["Lectura"]
                        ) for acc in data["sesionServicio"].get("accesoBD", [])
                    ]
                )
            )

            # 2. Guardar en Cascada
            db.add(respuesta)
            await db.commit()
            await db.refresh(respuesta)
            # return respuesta

        except Exception as e:
            db.rollback()
            raise e
        finally:
            await db.close()

    async def verify_payload_hash(self, db: AsyncSession, hash:str) -> bool:
        """
        Verifica de forma eficiente si un payload_hash ya está registrado en la BD.
        Retorna True si existe, False si no.
        """
        stmt = select(exists().where(Login.hash == hash))
        result = await db.execute(stmt)
        return result.scalar() or False
    

auth_repository = Auth_repository()