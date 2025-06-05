from sqlalchemy import Column, String, Float, ARRAY
from pgvector.sqlalchemy import Vector
from src.database import Base

from sqlalchemy import Column, String, Float, Text

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)  
    name = Column(String)
    description = Column(Text)
    color = Column(String)
    rating = Column(Float)
    url = Column(String)
    embedding = Column(Vector(1024))

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    gender = Column(String)
    location = Column(String)
    history_bought = Column(ARRAY(String))
    embedding = Column(Vector(1024))

