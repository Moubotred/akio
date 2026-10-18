from contextlib import asynccontextmanager
from fastapi import FastAPI,Request,HTTPException,status
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pathlib import Path

import redis.asyncio as aioredis

from app.core.database import engine
from app.core.base import Base

from app.core.exceptions import AppException

from app.frontend.router import frontend_router
from app.backend.router import backend as backend_router
from app.aplicacion.router import aplicacion as app_route

from app.core.logger import get_logger

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = aioredis.from_url("redis://localhost:6379", decode_responses=True)
    logger.info("[+] Redis iniciada")

    logger.info("[+] Base de datos iniciada")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    # await app.state.redis.close()


origins = [
    "https://tudominio.com",
    "https://dashboard.tudominio.com",
    "http://192.168.1.104:8080",  # IP interna específica si aplica
]


app = FastAPI(
    title="Akio Gateway",
    version="1.0.0",
    lifespan=lifespan
)

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # O tus orígenes explícitos
    allow_credentials=True,
    allow_methods=["*"],  # <-- Permite que OPTIONS y POST sean aceptados implícitamente
    allow_headers=["*"],  # <-- Permite 'ngrok-skip-browser-warning' y 'Content-Type'
)

@app.exception_handler(AppException)
async def auth_exception_handler(request: Request, exc: AppException):
    # Si intenta entrar a una ruta protegida sin permisos

    return JSONResponse(
        status_code=400,
        content={
            "categoria": exc.categoria,
            "mensajeAplicacion": "",
            "mensajeUsuario": exc.mensaje_usuario
        }
    )
    # if exc.status_code == status.HTTP_401_UNAUTHORIZED:
    #     # Redirige de inmediato a la pantalla de inicio de sesión
    #     return RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
    
    # return HTMLResponse(content=exc.detail, status_code=exc.status_code)

app.include_router(app_route)
app.include_router(frontend_router)
app.include_router(backend_router)
