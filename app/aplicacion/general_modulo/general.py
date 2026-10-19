from fastapi import (
    APIRouter,
    Depends,
    Body,
    Request
)

from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.core.proxy import Proxy_service
from app.core.lds_client import Lds_client
from app.core.logger import get_logger

logger = get_logger("General")

router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc",
    tags=["General"]
)

@router.post("/usuario")
async def registrar_suministro(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    get_info_user = await Proxy_service.post(db,"/usuario",payload,headers_server)  
    logger.debug(f"info: {get_info_user.content}")
    return JSONResponse(get_info_user.json(),200,headers_user)
