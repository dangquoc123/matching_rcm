import logging
from sqlalchemy.orm import Session
from src.services.embedding_service import EmbeddingService
from src.models import Product, User
from used.utils import extract_product_features

# logging.basicConfig(level=logging.INFO)

class VectorizationService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.embedding_service = EmbeddingService()

    def vectorize_products(self, products):
        for product in products:
            features = extract_product_features(product)
            vector = self.embedding_service.embed_text(features["text"])
            db_product = self.db.query(Product).filter(Product.id == features["id"]).first()
            if db_product:
                db_product.embedding = vector
            else:
                new_product = Product(id=features["id"], embedding=vector)
                self.db.add(new_product)
        self.db.commit()

    def vectorize_users(self, users):
        for user in users:
            vector = self.embedding_service.embed_user_profile(
                gender=user.gender,
                location=getattr(user, 'location', ''),
                history_bought=user.history_bought
            )
            db_user = self.db.query(User).filter(User.id == user.id).first()
            if db_user:
                db_user.embedding = vector
            else:
                new_user = User(id=user.id, embedding=vector)
                self.db.add(new_user)
        self.db.commit()







