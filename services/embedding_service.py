from sentence_transformers import SentenceTransformer
import numpy as np
from src.config import MODEL_EMBEDDING_NAME

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_EMBEDDING_NAME)

    def embed_text(self, text: str):
        return self.model.encode(text, normalize_embeddings=True)

    def embed_search_query(self, query: str):
        formatted = f"query: {query}"
        return self.model.encode(formatted, normalize_embeddings=True)

    def embed_clicked_product_description(self, description: str):
        formatted = f"passage: {description}"
        return self.model.encode(formatted, normalize_embeddings=True)

    def embed_user_history(self, recent_product_ids, product_vectors):
        vectors = []
        for pid in recent_product_ids:
            if pid in product_vectors:
                vectors.append(product_vectors[pid])
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return None

    def embed_user_profile(self, gender: str, location: str, history_bought: list, age: int = None):
        history_str = " ".join(history_bought) if history_bought else ""
        age_str = f", age: {age}" if age is not None else ""
        profile_text = f"gender: {gender}, location: {location}{age_str}, history: {history_str}"
        return self.model.encode(profile_text, normalize_embeddings=True)


