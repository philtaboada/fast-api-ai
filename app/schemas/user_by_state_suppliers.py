from pymongo.collection import Collection
from app.models.user_by_state_suppliers import UserByStateSupplier
from app.core.database import db
from fastapi import HTTPException
from pymongo.errors import PyMongoError

def save_state_supplier_data(data: UserByStateSupplier) -> str:
    suppliers_collection: Collection = db['users_by_state_suppliers']
    
    try:
        # Verifica si ya existe un documento con el mismo nombre
        existing_supplier = suppliers_collection.find_one({"name": data.name})
        
        if existing_supplier:
            # Si ya existe, no insertar y lanzar una excepción
            raise HTTPException(status_code=400, detail="The supplier already exists")
        
        # Inserta el documento en la colección
        result = suppliers_collection.insert_one(data.model_dump(by_alias=True))
        
        return str(result.inserted_id)
    
    except PyMongoError as e:
        # Maneja cualquier error relacionado con PyMongo
        raise HTTPException(status_code=500, detail=f"Error al guardar el proveedor: {str(e)}")

    except Exception as e:
        # Maneja otros errores generales
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")