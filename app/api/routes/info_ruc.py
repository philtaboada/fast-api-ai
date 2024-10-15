from fastapi import APIRouter, HTTPException
from app.schemas.info_ruc import search_by_ruc
from app.crud.info_ruc import createBusinessByRuc

info_ruc = APIRouter()

@info_ruc.get('/ruc/{ruc}')
async def business_by_ruc(ruc: str):
    # return {'ruc':ruc}
    try:
        # return {'nombre':'212'}
        return await createBusinessByRuc(ruc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))