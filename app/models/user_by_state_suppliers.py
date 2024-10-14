from typing import Dict, List, Optional
from pydantic import BaseModel

class Performance(BaseModel):
    stars: Optional[int] | None
    Sanciones_del_TCE: Optional[str] | None
    Penalidades: Optional[str] | None
    Inhabilitación_por_Mandato_Judicial: Optional[str] | None
    Inhabilitación_Administrativa: Optional[str] | None
    SUNAT: Optional[str] = None  
    SBS: Optional[str] = None

class AdditionalInfo(BaseModel):
    RUC: Optional[str] | None
    Teléfono: Optional[str] | None
    Email: Optional[str] | None
    Domicilio: Optional[str] | None
    CMC: Optional[str] | None
    CLC: Optional[str] | None
    Estado: Optional[str] | None
    Condición: Optional[str] | None
    Tipo_de_Contribuyente: Optional[str] | None

class ConformationSocietaria(BaseModel):
    Socios_Accionistas: Dict[str, str] 
    Representantes: Dict[str, str]
    Organos_Administracion: Dict[str, str]

class ExcelDataEntry(BaseModel):
    OBJETO: Optional[str]
    DESCRIPCION: Optional[str]
    ENTIDAD: Optional[str]
    MONEDA_DEL_MONTO_DEL_CONTRATO_ORIGINAL: Optional[str]
    MONTO_DEL_CONTRATO_ORIGINAL: Optional[float]
    FECHA_DE_FIRMA_DE_CONTRATO: Optional[str]
    FECHA_PREVISTA_DE_FIN_DE_CONTRATO: Optional[str]
    MIEMBROS_CONSORCIO: Optional[str]
    ESTADO: Optional[str]

class UserByStateSupplier(BaseModel):
    name: str
    current: Dict[str, str]
    performance: Performance
    additional_info: AdditionalInfo
    conformation_societaria: List[ConformationSocietaria]
    excel_data: List[ExcelDataEntry]




