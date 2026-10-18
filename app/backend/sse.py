# app/backend/sse.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import redis.asyncio as aioredis
from pydantic import BaseModel
import asyncio
import json

from app.core.constants import LDS
from app.core.database import get_redis

Event = APIRouter(prefix="/event", tags=["Server-Sent Events"])

class EventAppResponse(BaseModel):
    device_id: str
    status: str  # "approved" o "blocked"


@Event.post("/app")
async def listener_app(payload: EventAppResponse, redis: aioredis.Redis = Depends(get_redis)):
    device_id = payload.device_id
    status = payload.status.lower()

    if status == "approved":
        await redis.sadd(LDS.REDIS_APPROVED_SETS, device_id)
        await redis.srem(LDS.REDIS_BLOCKED_SETS, device_id)
    else:
        await redis.sadd(LDS.REDIS_BLOCKED_SETS, device_id)
        await redis.srem(LDS.REDIS_APPROVED_SETS, device_id)

    # PUBLICACIÓN CLAVE: Despierta a 'wait_for_device_approval' en auth_service.py
    device_channel = f"channel:device:{device_id}"
    await redis.publish(device_channel, json.dumps({"status": status}))

    return {"status": "ok", "action": status}


@Event.get("/web")
async def listerner_web(redis: aioredis.Redis = Depends(get_redis)):
    """Transmite eventos SSE globales hacia la aplicación web."""
    async def event_generator():
        async with redis.pubsub() as pubsub:
            await pubsub.subscribe("channel:approval:global")
            try:
                while True:
                    # Usar asyncio.shield o verificación de timeout
                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                    if message and message["type"] == "message":
                        data = message["data"]
                        if isinstance(data, bytes):
                            data = data.decode("utf-8")
                        yield f"data: {data}\n\n"
                    await asyncio.sleep(0.2)
            except asyncio.CancelledError:
                # Importante: relanzar para permitir que FastAPI limpìe la tarea
                raise
            finally:
                await pubsub.unsubscribe("channel:approval:global")

    return StreamingResponse(event_generator(), media_type="text/event-stream")