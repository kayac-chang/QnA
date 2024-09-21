from abc import abstractmethod
from typing import Protocol

from app.models.embedding import Embedding
from app.models.similarity_result import SimilarityResult


class VectorStore(Protocol):
    @abstractmethod
    async def add(self, *embeddings: Embedding) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: Embedding, k: int | None) -> list[SimilarityResult]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_sources(self, *sources: str) -> list[Embedding]:
        raise NotImplementedError

    @abstractmethod
    async def exist(self, source: str) -> bool:
        raise NotImplementedError
