import hashlib
from typing import TypedDict

import vecs as vecs
from app.config import settings
from app.models.embedding import Embedding
from app.models.similarity_result import SimilarityResult
from pydantic import TypeAdapter

name = "demo"


def hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


Record = tuple[str, float, TypedDict("Metadata", {"source": str})]


class SupabaseVectorStore:
    def __init__(self, dimensions: int):
        self.dimensions = dimensions

    async def add(self, *embeddings: Embedding) -> None:
        # create a new connection
        with vecs.create_client(settings.SUPABASE_DB_CONNECTION) as connection:
            # get or create the collection
            docs = connection.get_or_create_collection(
                name=name, dimension=self.dimensions
            )

            # upsert the embeddings
            docs.upsert(
                [
                    (
                        hash(e.source),  # hash(source) -> id
                        e.embedding,
                        {"source": e.source},
                    )
                    for e in embeddings
                ]
            )

            # create the index
            docs.create_index()

    async def search(self, query: Embedding, k: int = 1) -> list[SimilarityResult]:
        # create a new connection
        with vecs.create_client(settings.SUPABASE_DB_CONNECTION) as connection:
            # get or create the collection
            docs = connection.get_or_create_collection(
                name=name, dimension=self.dimensions
            )

            # search for the query
            res = docs.query(
                data=query.embedding,
                limit=k,  # number of records to return
                include_value=True,  # should distance measure values be returned?
                include_metadata=True,  # should record metadata be returned?
            )
            items = TypeAdapter(list[Record]).validate_python(res)

            # convert the results to SimilarityResult
            res = []
            for item in items:
                res.append(
                    SimilarityResult(
                        distance=item[1],
                        source=item[2]["source"],
                    )
                )

            return res
