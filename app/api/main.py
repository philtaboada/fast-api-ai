from fastapi import APIRouter

from app.api.routes import login, user, scraping_ruc, business, scraping_state_suppliers, pdf_routes, info_ruc

api = APIRouter() 

api.include_router(login.login, tags=["login"])
api.include_router(user.user, prefix="/user", tags=["user"])
api.include_router(scraping_ruc.scrapping_ruc, prefix="/scrapping_ruc", tags=["scrapping_ruc"])
api.include_router(info_ruc.info_ruc, prefix="/info_ruc", tags=["info_ruc"])
api.include_router(business.business, prefix="/business", tags=["business"])
api.include_router(scraping_state_suppliers.scraping_state_suppliers, prefix="/state_suppliers", tags=["state_suppliers"])
api.include_router(pdf_routes.router, prefix="/pdf", tags=["pdf"])
