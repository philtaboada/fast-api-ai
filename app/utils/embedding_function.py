import os
import google.generativeai as genai
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

API_OPEN_GEMINI = os.getenv("API_OPEN_GEMINI")

# Embedding function using gemini 

def get_embedding_function():
    # Configura tu API key
    genai.configure(api_key=API_OPEN_GEMINI  )
    
    # Crea y devuelve la función de embedding
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return embeddings

