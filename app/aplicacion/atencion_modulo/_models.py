# app/schemas/atencion.py

from typing import Optional, List
from pydantic import BaseModel


class Aplicacion(BaseModel):
    empresa: Optional[str] = None
    idPrograma: Optional[str] = None
    indSupervisor: Optional[str] = None
    nombreAplicacion: Optional[str] = None
    tipoAtencion: Optional[str] = None
    tipoEstado: Optional[str] = None


class ArchivoEstado(BaseModel):
    codigoEstado: Optional[str] = None
    codigoFSM: Optional[str] = None
    indObligatorio: Optional[str] = None
    tipoDocumento: Optional[str] = None


class EstadoSimple(BaseModel):
    ActFin: Optional[str] = None
    ActInicio: Optional[str] = None
    Anulable: Optional[str] = None
    AppAdrActivityInvoca: Optional[str] = None
    AppAdrInvoca: Optional[str] = None
    Asignable: Optional[str] = None
    CodigoFSM: Optional[str] = None
    Color: Optional[str] = None
    Confirmacion: Optional[str] = None
    Contable: Optional[str] = None
    DetieneTiempo: Optional[str] = None
    Estado: Optional[str] = None
    Id: Optional[str] = None
    IniciaTiempo: Optional[str] = None
    Manual: Optional[str] = None
    MuestraMapa: Optional[str] = None
    Nombre: Optional[str] = None
    ReqComentario: Optional[str] = None
    RequiereInfo: Optional[str] = None
    Tipo: Optional[str] = None


class Evento(BaseModel):
    CodigoFSM: Optional[str] = None
    Estado: Optional[EstadoSimple] = None
    EstadoEv: Optional[str] = None
    Id: Optional[str] = None
    Nombre: Optional[str] = None


class Estado(BaseModel):
    ActFin: Optional[str] = None
    ActInicio: Optional[str] = None
    Anulable: Optional[str] = None
    AppAdrActivityInvoca: Optional[str] = None
    AppAdrInvoca: Optional[str] = None
    Asignable: Optional[str] = None
    CodigoFSM: Optional[str] = None
    Color: Optional[str] = None
    Confirmacion: Optional[str] = None
    Contable: Optional[str] = None
    DetieneTiempo: Optional[str] = None
    Estado: Optional[str] = None
    Id: Optional[str] = None
    IniciaTiempo: Optional[str] = None
    ListadoEventos: List[Evento] = []
    Manual: Optional[str] = None
    MuestraMapa: Optional[str] = None
    Nombre: Optional[str] = None
    ReqComentario: Optional[str] = None
    RequiereInfo: Optional[str] = None
    Tipo: Optional[str] = None


class DatoDesplegable(BaseModel):
    codigoFSM: Optional[str] = None
    dato: Optional[str] = None
    keyDato: Optional[str] = None
    keyDatoPadre: Optional[str] = None
    valor: Optional[str] = None


class TipoDatoAtencion(BaseModel):
    codigoEstado: Optional[str] = None
    codigoFSM: Optional[str] = None
    idTipoDato: Optional[str] = None
    indObligatorio: Optional[str] = None
    keyTipoDato: Optional[str] = None
    keyTipoDatoPadre: Optional[str] = None
    labelTipoDato: Optional[str] = None
    listadoDesplegable: Optional[List[DatoDesplegable]] = None
    longitudDecimal: Optional[int] = None
    longitudEnteroDecimal: Optional[int] = None
    muestraSAD: Optional[str] = None
    tieneHijos: Optional[str] = None


class SubTipoAtencion(BaseModel):
    codigoFsmSubPedido: Optional[str] = None
    colorItem: Optional[int] = None
    descripcion: Optional[str] = None
    listadoEstados: List[Estado] = []
    subTipoAtencion: Optional[str] = None


class TipoAtencionCapataz(BaseModel):
    agregaFotoEjecutor: Optional[str] = None
    analizaFoto: Optional[str] = None
    asignaPorTipoAtencion: Optional[str] = None
    autoInicio: Optional[str] = None
    codigoFSM: Optional[str] = None
    comentarioEvento: Optional[str] = None
    descripcion: Optional[str] = None
    enviaAlerta: Optional[str] = None
    idAtencion: Optional[str] = None
    idProgramaAtencion: Optional[str] = None
    indValidaCuadrilla: Optional[str] = None
    iniciarPrimero: Optional[str] = None

    listadoAplicaciones: List[Aplicacion] = []
    listadoArchivoEstado: List[ArchivoEstado] = []
    listadoArchivosPersonales: List[dict] = []
    listadoCuadrillas: List[dict] = []
    listadoEstados: List[Estado] = []
    listadoPlacaAtencion: List[dict] = []
    listadoSubTipoAtencion: List[SubTipoAtencion] = []
    listadoTipoDatoAtencion: List[TipoDatoAtencion] = []

    modificaCodigoAtencion: Optional[str] = None
    ordenableApp: Optional[str] = None
    permiteAnadir: Optional[str] = None
    requiereJornada: Optional[str] = None
    requiereMarcaBase: Optional[str] = None
    requiereProcesamientoFinalizar: Optional[str] = None
    seleccionaPlaca: Optional[str] = None
    sinEventos: Optional[str] = None
    sinFotos: Optional[str] = None
    tieneSubtipoDocumento: Optional[str] = None
    tipoAtencion: Optional[str] = None
    unaALaVez: Optional[str] = None
    unaSolaAtencionCapataz: Optional[str] = None
    visiblePorGeocerca: Optional[str] = None


