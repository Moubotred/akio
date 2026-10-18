from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    JSON,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.core.base import Base


class TipoInstanciaSAD(Base):
    __tablename__ = "tipo_instancia_sad"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    instancia_listado_por_tipo: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    instancia_listado_total: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    payload: Mapped[dict] = mapped_column(
        JSON
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class SSTPlanificada(Base):
    __tablename__ = "sst_planificadas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_atencion_capataz: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    codigo_atencion: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    codigo_atencion_padre: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    tipo_atencion: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    subtipo_atencion: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    estado_cap: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    estado_cap_desc: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    tipo_estado: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )

    bloqueada: Mapped[bool] = mapped_column(
        default=False
    )

    prioritario: Mapped[bool] = mapped_column(
        default=False
    )

    payload: Mapped[dict] = mapped_column(
        JSON
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class TipoDocumentoAtencion(Base):
    __tablename__ = "tipo_documento_atencion"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_atencion_capataz: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    tipo_documento: Mapped[str] = mapped_column(
        String(50)
    )

    tipo: Mapped[str] = mapped_column(
        String(10)
    )

    descripcion: Mapped[str] = mapped_column(
        String(500)
    )

    obligatorio: Mapped[str] = mapped_column(
        String(5),
        nullable=True
    )

    orden: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    payload: Mapped[dict] = mapped_column(
        JSON
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Jornada(Base):
    __tablename__ = "jornadas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    imei_capataz: Mapped[str] = mapped_column(
        String(100)
    )

    tipo_atencion: Mapped[str] = mapped_column(
        String(100)
    )

    latitud: Mapped[float] = mapped_column(
        nullable=True
    )

    longitud: Mapped[float] = mapped_column(
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        default="INICIADA"
    )

    payload: Mapped[dict] = mapped_column(
        JSON
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
