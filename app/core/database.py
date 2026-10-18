from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from fastapi import Request
import redis.asyncio as aioredis
from contextlib import asynccontextmanager


from app.core.config import settings



engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Para las rutas FastAPI normales
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Para Tareas en Segundo Plano (BackgroundTasks)
@asynccontextmanager
async def get_db_ctx() -> AsyncGenerator[AsyncSession, None]:
    """
    Gestiona el ciclo de vida de la sesión para tareas en segundo plano.
    Abre la sesión y asegura su cierre al terminar el bloque 'async with'.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            # Si ocurre una excepción no capturada, hace rollback por seguridad
            await session.rollback()
            raise e
        finally:
            # Siempre se cierra la sesión liberando el pool
            await session.close()

async def get_redis(request: Request) -> aioredis.Redis:
    """Extrae la instancia de Redis almacenada en app.state"""
    return request.app.state.redis