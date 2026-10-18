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

router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc",
    tags=["General"]
)

@router.post("/usuario")
async def registrar_suministro(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    payload = await request.json()

    print(payload)
