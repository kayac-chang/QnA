from abc import abstractmethod
from typing import Protocol

from app.models.embedding import Embedding
from app.models.similarity_result import SimilarityResult


class VectorStore(Protocol):
    @abstractmethod
    async def add(self, *embeddings: Embedding) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: Embedding, k: int = 1) -> list[SimilarityResult]:
        raise NotImplementedError
