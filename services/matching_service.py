import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text
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
        
        # product_ids = [p.id for p in products]
        # product_texts = [f"{p.name} {p.description} {p.color}" for p in products]

        # Chuyển đổi query_vector thành chuỗi định dạng mảng SQL cho pgvector
        query_vector_str = str(query_vector.tolist())
        
        # Truy vấn SQL tối ưu, chỉ lấy các cột cần thiết
        sql_query = text("""
            SELECT id, name, description, color, 1 - (embedding <=> :query_vector) AS cosine_similarity
            FROM products
            WHERE embedding IS NOT NULL
            ORDER BY cosine_similarity DESC
            LIMIT 20
        """)
        
        # Thực thi truy vấn với query_vector
        result = self.db.execute(sql_query, {'query_vector': query_vector_str})
        top_products = result.fetchall()
        
        # Tạo mảng similarities và candidates từ kết quả SQL
        # similarities = np.array([row[4] for row in top_products])
        # top_20_idx = np.argsort(similarities)[-20:][::-1]
        candidates = [
            {"id": row[0], "text": f"{row[1]} {row[2]} {row[3]}"}
            for row in top_products[:20]
        ]

        reranked_ids = self.reranker.rerank(query_text, candidates, k=top_k)
        return reranked_ids