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

from app.aplicacion.registrar_modulo._service  import (
    Registrar_service
)

router = APIRouter(
    prefix="/inspeccion/registrar",
    tags=["Registrar"]
)

@router.post("/suministro")
async def registrar_suministro(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    payload = await request.json()

    print(payload)

    # return await Registrar_service.registrar_suministro(
    #     db=db,
    #     headers=dict(request.headers),
    #     payload=payload
    # )