# app/aplicacion/inspeccion_modulo/inspeccion.py

from fastapi import APIRouter,Depends,Request,Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.lds_client import Lds_client
from app.aplicacion.inspeccion_modulo._service  import Inspeccion_service

router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc/inspeccion",
    tags=["Inspeccion"]
)

@router.post("/suministro")
async def suministro(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    payload = await request.json()

    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)

    data = await Inspeccion_service.obtener_suministro(
        db=db,
        headers=dict(request.headers),
        payload=payload
    )
    return JSONResponse(data,200,headers_user)

    # return await Inspeccion_service.obtener_suministro(
    #     db=db,
    #     headers=dict(request.headers),
    #     payload=payload
    # )


@router.post("/tipofotos")
async def tipofotos(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await Inspeccion_service.obtener_suministro(
        db=db,
        headers=dict(request.headers),
        payload=payload
    )
    return JSONResponse(data,200,headers_user)
