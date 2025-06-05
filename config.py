from dotenv import load_dotenv
import os

load_dotenv()  

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")
MONGODB_USER_COLLECTION = os.getenv("MONGODB_USER_COLLECTION")
MODEL_EMBEDDING_NAME = os.getenv("MODEL_EMBEDDING_NAME")
MODEL_RERANK_NAME=os.getenv("MODEL_RERANK_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")


