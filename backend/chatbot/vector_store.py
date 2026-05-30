# =====================================================
# chatbot/vector_store.py
# =====================================================

import faiss
import numpy as np


class VectorStore:

    def __init__(self):

        self.index = None
        self.chunks = []

    def build_index(
        self,
        chunks,
        embeddings
    ):
        """
        Build FAISS index.
        """

        if len(chunks) == 0:
            return

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(
            np.array(
                embeddings,
                dtype=np.float32
            )
        )

        self.chunks = chunks

    def search(
    self,
    query_embedding,
    top_k=3
    ):

        if self.index is None:
            return []

        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32),
            top_k
        )

        results = []
        seen = set()

        for idx in indices[0]:

            if idx < len(self.chunks):

                chunk = self.chunks[idx]

                if chunk not in seen:
                    results.append(chunk)
                    seen.add(chunk)

        return results