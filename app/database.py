from pymongo import MongoClient
from app.config import MONGODB_URL, DATABASE_NAME


client = MongoClient(MONGODB_URL)

database = client[DATABASE_NAME]

analyses_collection = database["analyses"]