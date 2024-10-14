from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

conn = MongoClient(os.getenv("DB_HOST"))

db = conn.get_database()