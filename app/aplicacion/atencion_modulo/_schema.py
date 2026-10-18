# app/models/atencion.py

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

# from app.core.database import Base

from app.core.base import Base


class Atencion(Base):
    __tablename__ = "atenciones"

    tipo_atencion: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    descripcion: Mapped[str] = mapped_column(
        String(255)
    )

    codigo_fsm: Mapped[str] = mapped_column(
        String(100)
    )