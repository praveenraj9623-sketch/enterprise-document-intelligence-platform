from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RetrievalEngine:
    def __init__(self, method: str = "tfidf"):
        self.method = method
        self.chunks = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self.embedding_model = None
        self.embeddings = None
        self.active_method = "tfidf"

    def build_index(self, chunks: List[str]) -> str:
        self.chunks = chunks

        if self.method == "semantic":
            try:
                from sentence_transformers import SentenceTransformer

                self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
                self.embeddings = self.embedding_model.encode(
                    chunks,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                    show_progress_bar=False,
                )
                self.active_method = "semantic"
                return self.active_method
            except Exception:
                self.active_method = "tfidf"

        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=12000)
        self.tfidf_matrix = self.vectorizer.fit_transform(chunks)
        self.active_method = "tfidf"
        return self.active_method

    def search(self, query: str, top_k: int = 4) -> List[Dict]:
        if not self.chunks:
            return []

        if self.active_method == "semantic" and self.embedding_model is not None:
            query_embedding = self.embedding_model.encode(
                [query],
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            )[0]

            scores = np.dot(self.embeddings, query_embedding)
            top_indices = scores.argsort()[::-1][:top_k]

            return [
                {
                    "chunk_id": int(idx),
                    "score": float(scores[idx]),
                    "text": self.chunks[idx],
                }
                for idx in top_indices
            ]

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = scores.argsort()[::-1][:top_k]

        return [
            {
                "chunk_id": int(idx),
                "score": float(scores[idx]),
                "text": self.chunks[idx],
            }
            for idx in top_indices
        ]
