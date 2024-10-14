from fastapi import APIRouter

business = APIRouter()

@business.get("/business")
def get_business():
    return {"message": "Hello, world!"}

@business.post("/business")
def create_business():
    return {"message": "Hello, world!"}