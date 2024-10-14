from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.crud.scraping_state_suppliers import get_file_state_suppliers

scraping_state_suppliers = APIRouter()

@scraping_state_suppliers.get("/scraping")
async def state_suppliers():
    """
    Obtiene la información del Proveedor del estado, sus datos más importantes dentro del link de consulta 
    y ademas descargar el excel que contiene todos los contratos del Proveedor.

    Args:
        ruc_number (str): Número de RUC a consultar. Por defecto se usa "20603013540".
                                                           other ruc -> "20531654430"
    Returns:
        Dict: Un diccionario con los resultados de la consulta del Proveedor.
    """
    try:
        result = await run_in_threadpool(get_file_state_suppliers, ruc="20603013540")
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
