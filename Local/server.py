from pathlib import Path
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="AKIO Mock LDS")

# Tus JSON están en ~/Desktop/Log
LOG_DIR = Path(os.getcwd())


# ============================================================
# MAPEO DE RUTAS -> ARCHIVO DE RESPUESTA
# ============================================================

base = "/interno/platafadr/framework/lanzador/PltAndroid.svc"

ROUTES = {

    # Login
    f"{base}/Login/ValidaCredenciales":
        "ValidaCredenciales.json",

    f"{base}/Login/ParametrosIniciales":
        "ParametrosIniciales.json",

    f"{base}/Login/ValidarSesionActivaImei":
        "ValidarSesionActivaImei.json",

    f"{base}/Login/RegistrarUbicacion":
        "RegistrarUbicacion.json",

    # Capataz
    "/tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerTipoInstanciaSAD":
        "ObtenerTipoInstanciaSAD.json",

    "/tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerTipoDocumentoPorAtencion":
        "ObtenerTipoDocumentoPorAtencion.json",

    # Atención
    "/tecnicoi/spo/sad/atencion/Atencion.svc/Atencion/ObtenerTipoAtencionCapataz":
        "ObtenerTipoAtencionCapataz.json",

    # Inspección
    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/mapa/paquetestrabajo":
        "paquetestrabajo.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/mapa/paquetesinspeccion":
        "paquetesinspeccion.json",
    
   # Planificacion

    "/tecnicoi/spo/capataz/Capataz.svc/Capataz/ObtenerSSTMiPlanificacion":
        "ObtenerSSTMiPlanificacion.json",

    "/tecnicoi/spo/capataz/Capataz.svc/Capataz/IniciarJornada":
        "IniciarJornada.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/inspeccion/tipofotos":
        "tipofotos.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion/suministro":
         "conf_suministro.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/activo/poste/gradocorrosion":
         "gradocorrosion.json",
    
    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/usuario":
          "usuario.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/mapa/paquetesinspeccion":
          "paquetesinspeccion.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/inspeccion/cajatoma":
          "cajatoma.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion/llave":
          "llave.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion/valida/foto":
          "val_foto.json",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion/cajatoma":
          "conf_cajatoma",

    "/tecnicoii/GesManmtoBT/BTInspeccion.svc/configuracion/poste":
          "conf_poste"



}


# ============================================================
# CARGAR JSON
# ============================================================

def load_response(filename: str):

    filepath = LOG_DIR / "data" / filename

    if not filepath.exists():
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON inválido: {filepath}")
        print(e)
        return None


# ============================================================
# REQUEST LOGGER
# ============================================================

async def print_request(request: Request):

    body = await request.body()

    print()
    print("=" * 80)
    print("MOCK REQUEST")
    print("=" * 80)

    print(f"METHOD : {request.method}")
    print(f"PATH   : {request.url.path}")

    print()
    print("HEADERS:")
    for key, value in request.headers.items():
        print(f"  {key}: {value[70:]}")

    print()
    print("BODY:")

    if not body:
        print("  <EMPTY>")
        return

    try:
        data = json.loads(body)

        print(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            )
        )

    except Exception:
        print(f"  <BINARY {len(body)} bytes>")


# ============================================================
# POST GENÉRICO
# ============================================================

@app.post("/{path:path}")
async def mock_post(path: str, request: Request):


    await print_request(request)


    route = "/" + path.rstrip("/")
    print()
    print(f"ROUTE: {route}")


    # --------------------------------------------------------
    # Buscar respuesta
    # --------------------------------------------------------


    response_file = ROUTES.get(route)
    if response_file is None:
        print()
        print("[MOCK] ROUTE NO CONFIGURADA")

        print(f"[MOCK] {route}")


        return JSONResponse(

            status_code=404,

            content={

                "error": "Mock route not configured",

                "path": route

            }

        )


    # --------------------------------------------------------

    # Cargar JSON

    # --------------------------------------------------------


    response = load_response(response_file)


    if response is None:


        print()

        print("[MOCK] RESPONSE NO ENCONTRADO")

        print(f"[MOCK] Archivo: {response_file}")


        return JSONResponse(

            status_code=500,

            content={

                "error": "Mock response file not found",

                "file": response_file

            }

        )


    # --------------------------------------------------------

    # Responder

    # --------------------------------------------------------


    print()

    print("[MOCK] RESPONSE")

    print(f"[MOCK] {response_file}")


    print()

    print(

        json.dumps(

            response,

            indent=2,

            ensure_ascii=False

        )

    )


    print("=" * 80)


    return JSONResponse(

        status_code=200,

        content=response

    )


# ============================================================
# HEALTH
# ============================================================

@app.get("/")
async def root():

    return {
        "status": "ok",
        "server": "AKIO Mock LDS",
        "routes": len(ROUTES)
    }


@app.get("/health")
async def health():

    return {
        "status": "ok"
    }
