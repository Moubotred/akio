# app/models/login.py

from datetime import datetime


from typing import List, Optional
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.core.base import Base


from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy import DateTime, Integer, JSON,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship

# Request Usuario
# ----------------------------------------------------------------------
# TABLA DE LOGIN
# ----------------------------------------------------------------------
class Login(Base):
    __tablename__ = "login"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    hash:Mapped[str] = mapped_column(String(64),index=True)

    # Relaciones de uno a uno (Credenciales) y uno a muchos (Aplicaciones)
    credenciales: Mapped["Credential"] = relationship("Credential", back_populates="login", uselist=False, cascade="all, delete-orphan")
    aplicaciones_instaladas: Mapped[List["InstalledApp"]] = relationship("InstalledApp", back_populates="login", cascade="all, delete-orphan")

# ----------------------------------------------------------------------
# TABLA DE CREDENCIALES
# ----------------------------------------------------------------------
class Credential(Base):
    __tablename__ = "credenciales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login_id: Mapped[int] = mapped_column(ForeignKey("login.id", ondelete="CASCADE"), unique=True)
    
    usuario: Mapped[str] = mapped_column(String(50), index=True)
    password: Mapped[str] = mapped_column(String(255))
    dominio: Mapped[str] = mapped_column(String(100))
    empresa: Mapped[str] = mapped_column(String(20))
    empresa_contratante: Mapped[str] = mapped_column(String(20))
    id_dispositivo: Mapped[str] = mapped_column(String(100), index=True)
    version_android: Mapped[str] = mapped_column(String(20))
    version_plataforma: Mapped[str] = mapped_column(String(20))

    login: Mapped["Login"] = relationship("Login", back_populates="credenciales")

# ----------------------------------------------------------------------
#  TABLA DE APLICACION INSTALADAS
# ----------------------------------------------------------------------
class InstalledApp(Base):
    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login_id: Mapped[int] = mapped_column(ForeignKey("login.id", ondelete="CASCADE"))
    
    paquete: Mapped[str] = mapped_column(String(150))
    version: Mapped[str] = mapped_column(String(50))

    login: Mapped["Login"] = relationship("Login", back_populates="aplicaciones_instaladas")


# Response Servidor
# ----------------------------------------------------------------------
# TABLA PRINCIPAL: Respuesta / Sesión General
# ----------------------------------------------------------------------
class SessionResponse(Base):
    __tablename__ = "session_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(Text, nullable=False)
    disco_servidor_log: Mapped[Optional[str]] = mapped_column(String(50))
    path_servidor_log: Mapped[Optional[str]] = mapped_column(String(255))
    dias_restantes_caducar_clave: Mapped[Optional[int]] = mapped_column(Integer)
    info_plataforma: Mapped[Optional[str]] = mapped_column(String(255))
    rastrea_equipo: Mapped[bool] = mapped_column(Boolean, default=False)
    tiempo_rastreo: Mapped[Optional[int]] = mapped_column(Integer)
    requiere_mfa: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones
    aplicaciones: Mapped[List["Application"]] = relationship(
        "Application", back_populates="session_response", cascade="all, delete-orphan"
    )
    sesion_servicio: Mapped[Optional["ServiceSession"]] = relationship(
        "ServiceSession", back_populates="session_response", uselist=False, cascade="all, delete-orphan"
    )


# ----------------------------------------------------------------------
# TABLA: Aplicaciones
# ----------------------------------------------------------------------
class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_response_id: Mapped[int] = mapped_column(
        ForeignKey("session_responses.id", ondelete="CASCADE")
    )
    
    paquete: Mapped[str] = mapped_column(String(150), index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    version: Mapped[str] = mapped_column(String(50))
    obligatorio: Mapped[bool] = mapped_column(Boolean)
    id_plugin: Mapped[str] = mapped_column(String(50))
    es_favorito: Mapped[bool] = mapped_column(Boolean)
    es_visible: Mapped[bool] = mapped_column(Boolean)
    url: Mapped[Optional[str]] = mapped_column(String(255))

    # Relación
    session_response: Mapped["SessionResponse"] = relationship(
        "SessionResponse", back_populates="aplicaciones"
    )


# ----------------------------------------------------------------------
# TABLA: Sesión del Servicio
# ----------------------------------------------------------------------
class ServiceSession(Base):
    __tablename__ = "service_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_response_id: Mapped[int] = mapped_column(
        ForeignKey("session_responses.id", ondelete="CASCADE"), unique=True
    )

    id_sesion: Mapped[int] = mapped_column(BigInteger, index=True)
    id_dispositivo: Mapped[str] = mapped_column(String(100), index=True)
    token_id: Mapped[str] = mapped_column(String(50))
    ip_cliente: Mapped[str] = mapped_column(String(45))  # IPv4 / IPv6
    usuario_host: Mapped[Optional[str]] = mapped_column(String(100))
    token_sesion: Mapped[Optional[str]] = mapped_column(Text)

    # Relaciones (1:1 con Login y Usuario) y (1:N con Accesos a BD)
    session_response: Mapped["SessionResponse"] = relationship(
        "SessionResponse", back_populates="sesion_servicio"
    )
    login: Mapped[Optional["SessionLogin"]] = relationship(
        "SessionLogin", back_populates="service_session", uselist=False, cascade="all, delete-orphan"
    )
    usuario: Mapped[Optional["SessionUser"]] = relationship(
        "SessionUser", back_populates="service_session", uselist=False, cascade="all, delete-orphan"
    )
    accesos_bd: Mapped[List["DatabaseAccess"]] = relationship(
        "DatabaseAccess", back_populates="service_session", cascade="all, delete-orphan"
    )


# ----------------------------------------------------------------------
# TABLA: Detalle del Login dentro de Sesión
# ----------------------------------------------------------------------
class SessionLogin(Base):
    __tablename__ = "session_logins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_session_id: Mapped[int] = mapped_column(
        ForeignKey("service_sessions.id", ondelete="CASCADE"), unique=True
    )

    id_empresa: Mapped[int] = mapped_column(Integer)
    usuario: Mapped[str] = mapped_column(String(50))
    dominio: Mapped[str] = mapped_column(String(100))
    servidor: Mapped[Optional[str]] = mapped_column(String(100))
    servidor_remoto: Mapped[Optional[str]] = mapped_column(String(100))
    ruta_assemblies: Mapped[Optional[str]] = mapped_column(String(255))
    servidor_wcf: Mapped[Optional[str]] = mapped_column(String(100))
    key_dominio: Mapped[Optional[str]] = mapped_column(String(20))

    # Relación
    service_session: Mapped["ServiceSession"] = relationship(
        "ServiceSession", back_populates="login"
    )


# ----------------------------------------------------------------------
# TABLA: Usuario dentro de Sesión
# ----------------------------------------------------------------------
class SessionUser(Base):
    __tablename__ = "session_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_session_id: Mapped[int] = mapped_column(
        ForeignKey("service_sessions.id", ondelete="CASCADE"), unique=True
    )

    nombre: Mapped[str] = mapped_column(String(150))
    ficha: Mapped[Optional[str]] = mapped_column(String(50))
    cr: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    id_empresa_logeo: Mapped[int] = mapped_column(Integer)
    id_empresa_trabaja: Mapped[int] = mapped_column(Integer)
    usuario_logeo: Mapped[str] = mapped_column(String(50))
    rol: Mapped[Optional[str]] = mapped_column(String(100))  # Guardado como string (ej. "TRGV")

    # Relación
    service_session: Mapped["ServiceSession"] = relationship(
        "ServiceSession", back_populates="usuario"
    )


# ----------------------------------------------------------------------
# TABLA: Accesos BD (Lista amplia de Tags y Permisos)
# ----------------------------------------------------------------------
class DatabaseAccess(Base):
    __tablename__ = "database_accesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_session_id: Mapped[int] = mapped_column(
        ForeignKey("service_sessions.id", ondelete="CASCADE")
    )

    tag: Mapped[str] = mapped_column(String(100), index=True)
    escritura: Mapped[bool] = mapped_column(Boolean)
    lectura: Mapped[bool] = mapped_column(Boolean)

    # Relación
    service_session: Mapped["ServiceSession"] = relationship(
        "ServiceSession", back_populates="accesos_bd"
    )





# class Login(Base):
#     __tablename__ = "login"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True
#     )

#     username: Mapped[str] = mapped_column(
#         String(50),
#         index=True
#     )

#     device_id: Mapped[str | None] = mapped_column(
#         String(100),
#         nullable=True
#     )

#     success: Mapped[bool] = mapped_column(
#         Boolean
#     )

#     message: Mapped[str | None] = mapped_column(
#         String(500),
#         nullable=True
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         default=datetime.utcnow
#     )