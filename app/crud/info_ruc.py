from app.schemas.info_ruc import search_by_ruc, save_business_by_ruc_data
from pymongo.errors import PyMongoError
from fastapi import HTTPException

async def createBusinessByRuc(ruc):
  
  try:
    data = await search_by_ruc(ruc)
    
    saveData = save_business_by_ruc_data(data)
    print('se guardo: ', saveData)
    
    return data
  except PyMongoError as e:
    # Maneja cualquier error relacionado con PyMongo
    raise HTTPException(status_code=500, detail=f"Error al guardar el proveedor: {str(e)}")

  except Exception as e:
    # Maneja otros errores generales
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
  