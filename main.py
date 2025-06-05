import logging
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import service
from src.services.database_service import DatabaseService
from src.services.embedding_service import EmbeddingService
from src.services.matching_service import MatchingService

from src.utils.input_processor import InputProcessor
from src.handlers.recommendation_handler import RecommendationHandler

from src.config import DATABASE_URL

#logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# global variables
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()
db_service = DatabaseService(db_session)
embedding_service = EmbeddingService()
matching_service = MatchingService()

def main():
    input_processor = InputProcessor(logger)
    input_data = input_processor.process("input.json")

    handler = RecommendationHandler(
        db_service, embedding_service, matching_service, logger
    )
    handler.handle(input_data)


if __name__ == "__main__":
    main()
