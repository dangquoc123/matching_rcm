import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from src.database import SessionLocal
from src.models import Product, User
from src.services.rerank_service import RerankService

class MatchingService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.reranker = RerankService()

    def find_nearest_products(self, query_vector: np.ndarray, query_text: str, top_k: int = 10):
        products = self.db.query(Product).filter(Product.embedding != None).all()
        product_vectors = np.array([p.embedding for p in products])
        # check length
        if len(product_vectors) == 0:
            return []
        
        query_vector_str = str(query_vector.tolist())

        orm_query = (
            self.db.query(Product)
            .filter(Product.embedding != None)
            .order_by(func.cosine_distance(Product.embedding, query_vector_str))
            .limit(20)
        )
        result = orm_query.all()

        candidates = [
            {
                "id": product.id,
                "text": f"Name: {product.name or ''}. Description: {product.description or ''}. Color: {product.color or ''}."
            }
            for product in result
        ]
        # print("candidate : \n", candidates)

        reranked_ids = self.reranker.rerank(query_text, candidates, k=top_k)
        return reranked_ids
    
