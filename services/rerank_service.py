from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from src.config import MODEL_RERANK_NAME

class RerankService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_RERANK_NAME,
            trust_remote_code=True
            )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_RERANK_NAME,
            trust_remote_code=True
            )

    def rerank(self, query: str, candidate_products: list, k: int = 10):
        pairs = [(query, product["text"]) for product in candidate_products]
        inputs = self.tokenizer.batch_encode_plus(
            pairs, padding=True, truncation=True, return_tensors="pt"
        )
        with torch.no_grad():
            scores = self.model(**inputs).logits.squeeze(-1).numpy()
        top_indices = np.argsort(scores)[-k:][::-1]
        reranked = [candidate_products[i]["id"] for i in top_indices]
        return reranked
