from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import os
import sys
from src.config import DATABASE_NAME, DATABASE_PASSWORD

DATABASE_URL = f"postgresql+psycopg2://postgres:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    connection = engine.connect()
    connection.close()
    print("Database connect sucessfully")
except OperationalError as e:
    print("Error when connect database :", e)
    sys.exit(1)
except SQLAlchemyError as e:
    print("Error SQLAlchemy:", e)
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
