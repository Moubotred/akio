from fastapi import APIRouter

from app.aplicacion.login_modulo.login import router as aplicacion_Plataforma
from app.aplicacion.capataz_modulo.capataz import router as aplicacion_SAD
from app.aplicacion.activo_modulo.activo import router as aplicacion_Inpeccion

from app.aplicacion.atencion_modulo.atencion import router as sub_router_atencion
from app.aplicacion.mapa_modulo.mapa import router as sub_router_mapa
from app.aplicacion.general_modulo.general import router as sub_router_general
from app.aplicacion.configuracion_modulo.configuracion import router as sub_router_configuracion
from app.aplicacion.inspeccion_modulo.inspeccion import router as sub_router_inspeccion
from app.aplicacion.inspeccion_modulo._inspeccion_ import router as _sub_router_inspeccion_


# Router principal del backend que agrega el prefijo /api/v1
aplicacion = APIRouter(tags=["backend"])


# =====================================================
# Endoint principales de apps
# =====================================================
"""com.*.plataforma.movil"""
aplicacion.include_router(aplicacion_Plataforma)

"""com.*.proydist.sad"""
aplicacion.include_router(aplicacion_SAD)

"""com.*.bt.inspecciones.ui"""
aplicacion.include_router(aplicacion_Inpeccion)
# =====================================================


# =====================================================
# Endpoint secundarios de com.*.bt.inspecciones.ui
# =====================================================
# aplicacion.include_router(sub_router_atencion)
aplicacion.include_router(sub_router_mapa)
aplicacion.include_router(sub_router_general)
aplicacion.include_router(sub_router_configuracion)
aplicacion.include_router(sub_router_inspeccion)
aplicacion.include_router(_sub_router_inspeccion_)
# =====================================================
