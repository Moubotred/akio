import os
from pathlib import Path
from dotenv import load_dotenv

class LDS:

    load_dotenv()

    _DIR = Path(__file__).resolve().parent.parent

    REDIS_BLOCKED_SETS = "devices:blocked"
    REDIS_APPROVED_SETS = "devices:approved"
        
    REDIS_NOTIFICACIONES = "channel:approval:global"

    PROTOCOL = "https"

    DOMAIN = os.getenv("HOST_RED")
    # DOMAIN = os.getenv("HOST_REMOTO")

    BASE_URL = f"{PROTOCOL}://{DOMAIN}"

    SERVICES = {
        "LOGIN": "interno/platafadr/framework/lanzador/PltAndroid.svc",
        "CAPATAZ": "tecnicoi/spo/capataz/Capataz.svc/Capataz",
        "ARCHIVO": "tecnicoi/spo/sad/archivo/Archivo.svc/Archivo",
        "ATENCION": "tecnicoi/spo/sad/atencion/Atencion.svc/Atencion",
        "INSPECCION": "tecnicoii/GesManmtoBT/BTInspeccion.svc",
        "MAPA": "tecnicoii/GesManmtoBT/BTInspeccion.svc",
        "GENERAL": "tecnicoii/GesManmtoBT/BTInspeccion.svc",
        "ACTIVO": "tecnicoii/GesManmtoBT/BTInspeccion.svc/activo",
        "CONFIGURACION": "tecnicoii/GesManmtoBT/BTInspeccion.svc",
        "GIS": "tecnicoii/gisweb/sigred.svc"
    }

    ENDPOINTS = {

    "/ValidaCredenciales":
        ("LOGIN", "Login/ValidaCredenciales"),

    "/ParametrosIniciales":
        ("LOGIN", "Login/ParametrosIniciales"),

    "/ObtenerTipoInstanciaSAD":
        (
            "CAPATAZ",
            "ObtenerTipoInstanciaSAD"
        ),

    "/ObtenerSSTMiPlanificacion":
        (
            "CAPATAZ",
            "ObtenerSSTMiPlanificacion"
        ),

    "/IniciarJornada":
        (
            "CAPATAZ",
            "IniciarJornada"
        ),

    "/FinalizarJornada":
        (
            "CAPATAZ",
            "FinalizarJornada"
        ),

    "/ObtenerTipoAtencionCapataz":
        (
            "ATENCION",
            "ObtenerTipoAtencionCapataz"
        ),

    "/ObtenerTipoDocumentoPorAtencion":
        (
            "ATENCION",
            "ObtenerTipoDocumentoPorAtencion"
        ),

    "/paquetestrabajo":
        (
            "MAPA",
            "mapa/paquetestrabajo"
        ),

    "/paquetesinspeccion":
        (
            "MAPA",
            "mapa/paquetesinspeccion"
        ),
    "/conf/suministro":
        (
            "CONFIGURACION",
            "configuracion/suministro"
        ),
    "/ObtenerTipoDocumentoPorAtencion":
        (
            "ARCHIVO",
            "ObtenerTipoDocumentoPorAtencion"
        ),
    "/regis/suministro":
        (
            "INSPECCION",
            "/inspeccion/registrar/suministro"
        ),
    "/usuario":
        (
            "GENERAL",
            "usuario"
        )
    
    }