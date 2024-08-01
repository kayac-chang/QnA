import faiss
import numpy as np
from app.models.embedding import Embedding
from app.models.similarity_result import SimilarityResult


class FaissVectorStore:
    def __init__(self, dimensions: int):
        self.store: list[Embedding] = []
        self.index = faiss.IndexFlatL2(dimensions)

    async def add(self, *embeddings: Embedding) -> None:
        """Add embeddings to the store and index"""

        # extend the store with the new embeddings
        self.store.extend(embeddings)

        # add the new embeddings to the index
        for embedding in embeddings:
            self.index.add(np.array([embedding.embedding], dtype=np.float32))  # type: ignore

    async def search(self, query: Embedding, k: int = 1) -> list[SimilarityResult]:
        """Search for similar embeddings in the store"""

        # search for the query in the index
        np_query = np.array([query.embedding], dtype=np.float32)
        distances, indices = self.index.search(np_query, k)  # type: ignore

        return [
            SimilarityResult(distance=distance, source=self.store[index].source)
            for distance, index in zip(distances[0], indices[0])
        ]
