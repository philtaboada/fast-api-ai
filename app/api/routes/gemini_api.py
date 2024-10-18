from fastapi import APIRouter

gemini_api = APIRouter()

@gemini_api.get("/gemini")
def get_gemini():
    return {"message": "Hello, world!"}