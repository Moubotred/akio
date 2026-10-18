from pydantic import BaseModel


class ObtenerTipoDocumentoPorAtencionRequest(
    BaseModel
):
    tipoAtencion: str
    idAtencionCapataz: str


class JornadaDTO(BaseModel):
    imeiCapataz: str
    latitud: float
    longitud: float
    tipoAtencion: str


class IniciarJornadaRequest(BaseModel):
    jornadaDto: JornadaDTO


class FinalizarJornadaRequest(BaseModel):
    jornadaDto: JornadaDTO
