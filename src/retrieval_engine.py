import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RetrievalEngine:
    def __init__(self, method="tfidf"):
        self.method = method
        self.chunks = []
        self.active_method = "tfidf"

        self.vectorizer = None
        self.tfidf_matrix = None

        self.embedding_model = None
        self.embeddings = None

    def build_index(self, chunks):
        self.chunks = chunks

        if not chunks:
            self.active_method = "none"
            return self.active_method

        if self.method == "semantic":
            try:
                from sentence_transformers import SentenceTransformer

                # Lightweight model suitable for Streamlit Cloud deployment
                self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

                texts = [chunk["text"] if isinstance(chunk, dict) else str(chunk) for chunk in chunks]

                self.embeddings = self.embedding_model.encode(
                    texts,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                    show_progress_bar=False,
                )

                self.active_method = "semantic"
                return self.active_method

            except Exception as error:
                print(f"Semantic search failed. Falling back to TF-IDF. Error: {error}")
                self.active_method = "tfidf"

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2),
        )

        texts = [chunk["text"] if isinstance(chunk, dict) else str(chunk) for chunk in chunks]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

        self.active_method = "tfidf"
        return self.active_method

    def search(self, query, top_k=3):
        if not self.chunks:
            return []

        if self.active_method == "semantic" and self.embedding_model is not None:
            query_embedding = self.embedding_model.encode(
                [query],
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            scores = np.dot(self.embeddings, query_embedding[0])
            top_indices = np.argsort(scores)[::-1][:top_k]

            results = []
            for idx in top_indices:
                chunk = self.chunks[idx]
                text = chunk["text"] if isinstance(chunk, dict) else str(chunk)
                chunk_id = chunk.get("chunk_id", idx) if isinstance(chunk, dict) else idx

                results.append(
                    {
                        "chunk_id": chunk_id,
                        "text": text,
                        "score": float(scores[idx]),
                    }
                )

            return results

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            text = chunk["text"] if isinstance(chunk, dict) else str(chunk)
            chunk_id = chunk.get("chunk_id", idx) if isinstance(chunk, dict) else idx

            results.append(
                {
                    "chunk_id": chunk_id,
                    "text": text,
                    "score": float(scores[idx]),
                }
            )

        return results