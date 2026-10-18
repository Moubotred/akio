from fastapi import APIRouter

from app.aplicacion.login_modulo.login import router as aplicacion_Plataforma
from app.aplicacion.capataz_modulo.capataz import router as aplicacion_SAD
from app.aplicacion.activo_modulo.activo import router as aplicacion_Inpeccion


from app.aplicacion.atencion_modulo.atencion import router as atencion
from app.aplicacion.mapa_modulo.mapa import router as mapa
# from app.aplicacion.activo_modulo.activo import router as activo


# Router principal del backend que agrega el prefijo /api/v1
aplicacion = APIRouter(tags=["backend"])

# Anidamos los subrouters
aplicacion.include_router(aplicacion_Plataforma)
aplicacion.include_router(aplicacion_SAD)
aplicacion.include_router(aplicacion_Inpeccion)


aplicacion.include_router(atencion)
aplicacion.include_router(mapa)
# aplicacion.include_router(activo)