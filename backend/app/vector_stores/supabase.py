import vecs
from app.config import settings
from app.models.embedding import Embedding
from app.models.similarity_result import SimilarityResult

vx = vecs.create_client(settings.SUPABASE_DB_CONNECTION)


class SupabaseVectorStore:
    def __init__(self, dimensions: int): ...

    async def add(self, *embeddings: Embedding) -> None: ...

    async def search(self, query: Embedding, k: int = 1) -> list[SimilarityResult]: ...
