from typing_extensions import Annotated
from pydantic import BaseModel, StringConstraints

class EmpresaApiNet(BaseModel):
    razonSocial: str
    tipoDocumento: Annotated[str, StringConstraints(min_length=1, max_length=10)]
    numeroDocumento: Annotated[str, StringConstraints(min_length=8, max_length=11)]
    estado: str
    condicion: str
    direccion: str
    ubigeo: str
    viaTipo: str
    viaNombre: str
    zonaCodigo: str
    zonaTipo: str
    numero: str
    interior: str
    lote: str
    dpto: str
    manzana: str
    kilometro: str
    distrito: str
    provincia: str
    departamento: str
    EsAgenteRetencion: bool
    tipo: str
    actividadEconomica: str
    numeroTrabajadores: str  
    tipoFacturacion: str
    tipoContabilidad: str
    comercioExterior: str