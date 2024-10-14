from typing import Optional
from pydantic import BaseModel, Field

class ConsultaRuc(BaseModel):
    numeroRuc: str
    tipoContribuyente: str
    tipoDeDocumento: str
    nombreComercial: str
    fechaDeInscripcion: str
    estadoDelContribuyente: str
    condicionDelContribuyente: str
    domicilioFiscal: str
    sistemaEmisionDeComprobante: str
    actividadComercioExterior: str
    sistemaContabilidad: str
    actividadesEconomicas: str
    comprobantesDePagoCuImpresos: str
    sistemaDeEmisionElectronica: str
    emisorElectronicoDesde: str
    comprobantesElectronicos: str
    afiliadoAlPleDesde: str
    padrones: str
    fechaDeInicioDeActividades: Optional[str] = None

class LegalAgent(BaseModel):
    Documento: str
    NroDocumento: str = Field(..., alias="Nro. Documento")
    Nombre: str
    Cargo: str
    FechaDesde: str = Field(..., alias="Fecha Desde")

class UserByRuc(BaseModel):
    consulta_ruc: ConsultaRuc
    legal_agent: LegalAgent