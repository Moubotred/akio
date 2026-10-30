from fastapi import APIRouter,Request,Body,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.aplicacion.activo_modulo._service import activo_service
from app.core.database import get_db
from app.core.logger import get_logger
from app.core.lds_client import Lds_client


logger = get_logger("activo")

router = APIRouter(
    prefix="/tecnicoii/GesManmtoBT/BTInspeccion.svc/activo",
    tags=["Activo"]
)

@router.post("/poste/gradocorrosion")
async def obtener_grado_corrocion(
    request: Request,
    db: AsyncSession = Depends(get_db),
    payload: dict = Body(default={}),
):
    headers_server = dict(request.headers)
    headers_user = Lds_client.sanitize_headers(headers_server)
    data = await activo_service.obtener_grado_corrocion(db,headers_server,payload)
    # logger.debug(f"[-] Gradocorrocion {data.content}")
    return JSONResponse(data.json(),200,headers_user)
