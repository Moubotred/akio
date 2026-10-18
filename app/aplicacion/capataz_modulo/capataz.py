from fastapi import APIRouter,Depends,Request,BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.tasks import bd_background_sst
from app.core.proxy import Proxy_service
from app.core.lds_client import Lds_client
from app.aplicacion.capataz_modulo._service  import Capataz_service

router = APIRouter(
    prefix="/tecnicoi/spo/capataz/Capataz.svc/Capataz",
    tags=["Capataz"]
)

# async def bd_background(db, payload, headers):
#     # Aquí sí haces una petición normal con JSON completo porque corre en segundo plano
#     response = await Lds_client.post("/ObtenerSSTMiPlanificacion",payload,headers)
#     datos = response.json()

# ObtenerTipoAtencionCapataz
@router.post(
    "/ObtenerTipoInstanciaSAD"
)
async def obtener_tipo_instancia_sad(
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    payload = await request.json()

    return await Capataz_service.obtener_tipo_instancia_sad(
        db=db,
        headers=dict(request.headers),
        payload=payload
    )

# app/aplicacion/capataz_modulo/capataz
@router.post(
    "/ObtenerSSTMiPlanificacion"
)
async def obtener_sst_mi_planificacion(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    
    # Fuentes:
    #     https://gemini.google.com/app/9aa276277eb8cc6e
    #     https://share.google/aimode/0tQ4B7Am63iFw41Eq
    # 
    # Archivo referentes:  
    #     /home/kimshizi/Desktop/Log/v4/app/core/clients/gateway.py
    #     /home/kimshizi/Desktop/Log/v4/app/core/FakeForwarding.py 

    payload = await request.json()
    headers = dict(request.headers)

    filtered_headers = {
        k: v for k, v in headers.items()
        if k.lower() not in {"content-length", "transfer-encoding", "connection", "host","x-forwarded-proto","accept-encoding","x-forwarded-for","x-forwarded-host"}
    }

    # 1 - Tarea en segundo plano
    background_tasks.add_task(
        bd_background_sst, 
        db, 
        payload, 
        dict(request.headers)
    )
    
    # 2 - Peticion en tiempo real para usuario
    stream_generator = Capataz_service.obtener_sst_mi_planificacion_stream(
        db=db,
        headers=headers,
        payload=payload
    )

    # 3. Retornar StreamingResponse al cliente sin esperas
    return StreamingResponse(
        stream_generator,
        status_code=200,
        headers=filtered_headers)


@router.post(
    "/IniciarJornada"
)
async def obtener_inicio_jornada(
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    payload = await request.json()

    return await Capataz_service.obtener_tipo_instancia_sad(
        db=db,
        headers=dict(request.headers),
        payload=payload
    )


# @router.post(
#     "/FinalizarJornada"
# )
# async def obtener_finalizacion_jornada(
#     request: Request,
#     db: AsyncSession = Depends(get_db)
# ):

#     payload = await request.json()

#     return await Capataz_service.obtener_tipo_instancia_sad(
#         db=db,
#         headers=dict(request.headers),
#         payload=payload
#     )


# @router.post(
#     "/ObtenerTipoDocumentoPorAtencion"
# )
# async def obtener_tipo_documento_por_atencion(
#     request: Request,
#     db: AsyncSession = Depends(get_db)
# ):

#     payload = await request.json()

#     return await Capataz_service.obtener_tipo_documento_por_atencion(
#         db=db,
#         headers=dict(request.headers),
#         payload=payload
#     )