# utils/mongo_handler.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["chatbotDB"]
pdfs_collection = db["pdfs"]

def save_pdf_to_mongo(filename: str, content: bytes):
    existing = pdfs_collection.find_one({"filename": filename})
    if existing:
        pdfs_collection.update_one(
            {"filename": filename},
            {"$set": {"content": content}}
        )
    else:
        pdfs_collection.insert_one({
            "filename": filename,
            "content": content
        })
