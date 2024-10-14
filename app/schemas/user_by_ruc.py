from pymongo.collection import Collection
from app.models.user_by_ruc import UserByRuc, ConsultaRuc, LegalAgent
from app.core.database import db
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import PyMongoError

def user_by_ruc_schema(id: str) -> dict:
    try:
        # Convierte el id en ObjectId y busca el usuario en la base de datos
        user = db['users_by_ruc'].find_one({"_id": ObjectId(id)})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Devuelve el usuario formateado
        return {
            # "id": str(user['_id']),
            # "consulta_ruc": user.get('consulta_ruc', {}),
            # "legal_agent": user.get('legal_agent', {}),   
            "id": str(user['_id']),
            "consulta_ruc": ConsultaRuc(**user.get('consulta_ruc', {})).model_dump(),
            "legal_agent": LegalAgent(**user.get('legal_agent', {})).model_dump(),
        }
    
    except PyMongoError as e:
        # Maneja errores relacionados con MongoDB
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        # Maneja otros errores generales
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

def users_by_ruc_schema() -> list:
    try:
        users_cursor = db['users_by_ruc'].find()
        
        # Se usa user_by_ruc_schema para formatear los usuarios y convertir cada uno en un diccionario
        return [user_by_ruc_schema(user['_id']) for user in users_cursor]
    
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

def save_user_ruc_data(data: UserByRuc) -> str:
    # Accede a la colección donde debe almacenar los datos
    users_collection: Collection = db['users_by_ruc']
    
    try:
        # Busca un documento existente con el mismo numeroRuc
        found_user = users_collection.find_one({"consulta_ruc.numeroRuc": data.consulta_ruc.numeroRuc})
        
        if found_user:
            # Si el usuario ya existe, no se realiza la inserción
            return "There is already an existing user with that ruc number."
        
        # Inserta el documento en la colección
        result = users_collection.insert_one(data.model_dump(by_alias=True))
        
        return str(result.inserted_id)
    
    except PyMongoError as e:
        # Maneja cualquier error relacionado con PyMongo
        raise HTTPException(status_code=500, detail=f"Error al guardar el usuario: {str(e)}")