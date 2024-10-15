from fastapi import HTTPException
from pymongo.errors import PyMongoError

from pymongo.collection import Collection
from app.core.database import db


from app.models.info_ruc import EmpresaApiNet

import httpx

async def search_by_ruc(ruc: str) -> EmpresaApiNet:
    # print(id)
    # return {"ruc": id, "nombre": "Empresa XYZ"}
    # try:
        headers = { 'Authorization': f'Bearer apis-token-11017.2xF2UEJuhOPSBc5YUY6Sm0uMNvvYr1Wx', 'Accept': 'application/json' }
        
        r = httpx.get(f"https://api.apis.net.pe/v2/sunat/ruc/full?numero={ruc}", headers=headers)
        
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail="Error fetching data from API")
    
        # Convierte el JSON a un modelo de Pydantic
        try:
            data = EmpresaApiNet(**r.json())  # Aquí creas una instancia del modelo
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")
        
        return data

def save_business_by_ruc_data(data: EmpresaApiNet) -> dict:
    business_by_ruc_collection: Collection = db['business_by_ruc']
    print('se busco: ', data.numeroDocumento)
    try:
        # Verifica si ya existe un documento con el mismo nombre
        existing_supplier = business_by_ruc_collection.find_one({"numeroDocumento": data.numeroDocumento})
        
        if existing_supplier:
            # Si ya existe, no insertar y lanzar una excepción
            raise HTTPException(status_code=400, detail="The business already exists")
        
        # Inserta el documento en la colección
        result = business_by_ruc_collection.insert_one(data.model_dump(by_alias=True))
        
        return { "message": "The business was created successfully" }
    
    except PyMongoError as e:
        # Maneja cualquier error relacionado con PyMongo
        raise HTTPException(status_code=500, detail=f"Error al guardar el proveedor: {str(e)}")

    except Exception as e:
        # Maneja otros errores generales
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")