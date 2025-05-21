import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, index_path="vector_index", model_name="all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.texts = []  # to map index back to text
        self.index = faiss.IndexFlatL2(self.dim)

        # Load index if exists
        self._load()

    def add(self, text):
        embedding = self.model.encode([text])
        self.index.add(embedding)
        self.texts.append(text)
        self._save()

    def query(self, text, top_k=1):
        if len(self.texts) == 0:
            return []

        query_embedding = self.model.encode([text])
        distances, indices = self.index.search(query_embedding, top_k)

        return [self.texts[i] for i in indices[0] if i < len(self.texts)]

    def _save(self):
        faiss.write_index(self.index, f"{self.index_path}.faiss")
        with open(f"{self.index_path}.pkl", "wb") as f:
            pickle.dump(self.texts, f)

    def _load(self):
        if os.path.exists(f"{self.index_path}.faiss") and os.path.exists(f"{self.index_path}.pkl"):
            self.index = faiss.read_index(f"{self.index_path}.faiss")
            with open(f"{self.index_path}.pkl", "rb") as f:
                self.texts = pickle.load(f)

    def clear(self):
        self.index = faiss.IndexFlatL2(self.dim)
        self.texts = []
        self._save()
    
    def delete(self, text_to_remove):
        # Find exact match index
        if text_to_remove in self.texts:
            idx = self.texts.index(text_to_remove)
            self.texts.pop(idx)
            # Rebuild index from scratch
            new_embeddings = self.model.encode(self.texts)
            self.index = faiss.IndexFlatL2(self.dim)
            if len(self.texts) > 0:
                new_embeddings = self.model.encode(self.texts)
                self.index.add(new_embeddings)
            self._save()
            return True
        return False

