# app/aplicacion/inspeccion_modulo/inspeccion.py

from fastapi import (
    APIRouter,
    Depends,
    Request
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.aplicacion.inspeccion_modulo._service  import (
    Inspeccion_service
)

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

    return await Inspeccion_service.obtener_suministro(
        db=db,
        headers=dict(request.headers),
        payload=payload
    )


    # return await Inspeccion_service.obtener_suministro(
    #     db=db,
    #     headers=dict(request.headers),
    #     payload=payload
    # )


@router.post("/tipofotos")
async def tipofotos(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    pass

    # return await Inspeccion_service.obtener_suministro(
    #     db=db,
    #     headers=dict(request.headers),
    #     payload=payload
    # )
