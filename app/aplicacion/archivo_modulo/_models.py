from pydantic import BaseModel


class TipoDocumentoResponse(BaseModel):

    descripcion: str

    tipo: str

    tipoDocumento: str

    obligatorio: str | None = None

    orden: int | None = None
