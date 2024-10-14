from fastapi import APIRouter

user = APIRouter()

@user.get("/users")
def get_users():
    return {"message": "Hello, world!"}