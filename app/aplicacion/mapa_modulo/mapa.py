from fastapi import (
    APIRouter,
    Depends,
    Request,
    Body
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.aplicacion.mapa_modulo._service  import (
    Mapa_service
)


router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc/mapa",
    tags=["Mapa"]
)

@router.post(
    "/paquetestrabajo"
)
async def obtener_paquetes_trabajo(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Mapa_service.obtener_paquetes_trabajo(
        db,
        payload=payload,
        headers=dict(request.headers)
    )
@router.post(
   "/paquetesinspeccion"
)
async def obtener_paquetes_inspeccion(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    return await Mapa_service.obtener_paquetes_inspeccion(
        db,
        payload=payload,
        headers=dict(request.headers)
    )

