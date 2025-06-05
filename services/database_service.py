from sqlalchemy.orm import Session
from src.models import Product, User

class DatabaseService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user_vector(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user.embedding if user else None

    def get_product_by_id(self, product_id):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_product_vector(self, product_id):
        product = self.get_product_by_id(product_id)
        return product.embedding if product else None

    def get_history_product_vectors(self, product_ids):
        return (
            self.session.query(Product)
            .filter(Product.id.in_(product_ids))
            .filter(Product.embedding.isnot(None))
            .all()
        )