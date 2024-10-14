from fastapi import APIRouter

login = APIRouter()

@login.get("/login")
def get_users():
    return {"message": "Hello, world!"}