# app/models/tipo_documento.py

class TipoDocumento(Base):

    __tablename__ = "tipo_documentos"

    id = mapped_column(
        primary_key=True
    )

    id_atencion_capataz = mapped_column(
        String,
        index=True
    )

    tipo_atencion = mapped_column(
        String
    )

    tipo = mapped_column(
        String
    )

    tipo_documento = mapped_column(
        String
    )

    descripcion = mapped_column(
        String
    )

    obligatorio = mapped_column(
        String
    )

    orden = mapped_column(
        Integer
    )
