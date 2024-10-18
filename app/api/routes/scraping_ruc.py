from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.crud.scrapping_ruc import get_info_ruc
from app.crud.rucNumber import RucNumber
from app.core.database import db
from app.schemas.user_by_ruc import user_by_ruc_schema, users_by_ruc_schema
from bson import ObjectId

scrapping_ruc = APIRouter()

@scrapping_ruc.get('/users_ruc', response_model=list)
async def find_all_user():
    try:
        return users_by_ruc_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@scrapping_ruc.get('/users_ruc/{id}', response_model=dict)
async def find_user(id: str):
    try:
        return user_by_ruc_schema(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@scrapping_ruc.post("/scrapping_ruc")
async def post_ruc():
    """
    Obtiene la información del RUC y sus datos más importantes dentro del link de consulta RUC.

    Args:
        ruc_number (str): Número de RUC a consultar. Por defecto se usa "20611519347".

    Returns:
        Dict: Un diccionario con los resultados de la consulta del RUC.
    """
    try:
        result = await run_in_threadpool(get_info_ruc, ruc_number="20604944903")
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

