from pydantic import BaseModel
from typing import Any

from pydantic import BaseModel, Field


class AplicacionInstalada(BaseModel):
    paquete: str
    version: str

class Credenciales(BaseModel):
    dominio: str
    empresa: str
    empresaContratante: str
    idDispositivo: str
    password: str
    usuario: str
    versionAndroid: str
    versionPlataforma: str

class SolicitudDispositivo(BaseModel):
    aplicacionesInstaladas: list[AplicacionInstalada] = Field(
        default_factory=list
    )
    credenciales: Credenciales

class ParametrosIniciales(BaseModel):
    imei: str
    ultimaEmpresaLogea: str
    ultimaEmpresaTrabaja: str
    ultimoDominio: str
    ultimoUsuario: str

class SolicitudParametros(BaseModel):
    paramIniciales: ParametrosIniciales

class DynamicPayload(BaseModel):
    model_config = {
        "extra": "allow"
    }

class TerminarPayload(BaseModel):
    token: dict[str, Any]

