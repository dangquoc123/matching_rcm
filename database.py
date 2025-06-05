from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import os
import sys

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql+psycopg2://postgres:Pass1234!@localhost:5432/postgres"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    connection = engine.connect()
    connection.close()
    print("Kết nối database thành công.")
except OperationalError as e:
    print("Lỗi kết nối tới database:", e)
    sys.exit(1)
except SQLAlchemyError as e:
    print("Lỗi SQLAlchemy:", e)
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
