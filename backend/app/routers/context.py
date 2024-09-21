from typing import Literal
from uuid import UUID, uuid4

import app.constants as CONST
import app.models as models
import app.services.completions as completions
import app.services.embeddings as embeddings
import app.vector_stores as vector_stores
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class Context:
    def __init__(
        self,
        embedding_model: CONST.TYPE_SUPPORTED_EMBEDDING_MODEL,
        vector_store: vector_stores.VectorStore,
    ):
        self.embedding_model: CONST.TYPE_SUPPORTED_EMBEDDING_MODEL = embedding_model
        self.vector_store: vector_stores.VectorStore = vector_store


stores: dict[UUID, Context] = {}

router = APIRouter(
    prefix="/context",
    tags=["context"],
)


class ContextCreateRequest(BaseModel):
    embedding_model: CONST.TYPE_SUPPORTED_EMBEDDING_MODEL
    vector_store: Literal["faiss", "supabase"]
    sources: list[str]


@router.post("/")
async def create_context(request: ContextCreateRequest) -> str:
    # generate a new id
    id = uuid4()

    # create the vector store based on the request
    vector_store: vector_stores.VectorStore
    match request.vector_store:
        case "faiss":
            vector_store = vector_stores.FaissVectorStore(
                dimensions=CONST.EMBEDDING_DIMENSIONS[request.embedding_model]
            )
        case "supabase":
            vector_store = vector_stores.SupabaseVectorStore(
                dimensions=CONST.EMBEDDING_DIMENSIONS[request.embedding_model]
            )
        case _:
            raise HTTPException(status_code=400, detail="invalid vector store")

    # create a new context
    stores[id] = Context(
        embedding_model=request.embedding_model,
        vector_store=vector_store,
    )

    try:

        async def add_to_store(*sources: str):
            existed_sources = [
                embedding.source
                for embedding in await stores[id].vector_store.get_all_by_sources(
                    *sources
                )
            ]
            new_sources = list(set(sources) - set(existed_sources))

            # generate embeddings for the sources
            generated_embeddings = await embeddings.generate(
                input=new_sources, model=request.embedding_model
            )

            # add the generated embeddings to the context
            await stores[id].vector_store.add(*generated_embeddings)

        # add the sources to the store
        await add_to_store(*request.sources)

        # return the id of the context
        return str(id)
    except Exception as e:
        # log the error
        print(e)

        # if there is an error, remove the context
        stores.pop(id)

        raise HTTPException(status_code=500, detail="error while creating context")


@router.get("/{context_id}/search")
async def search(
    context_id: UUID, query: str, k: int | None
) -> list[models.SimilarityResult]:
    # find context by id
    context = stores.get(context_id)

    # if context not found, return 404
    if context is None:
        raise HTTPException(status_code=404, detail="context not found")

    # generate embeddings for the query
    query_embedding = await embeddings.generate(
        input=query, model=context.embedding_model
    )

    # search the store for the query embedding
    return await context.vector_store.search(query_embedding[0], k=k)


@router.get("/{context_id}/qna")
async def qna(context_id: UUID, question: str):

    results = await search(context_id=context_id, query=question, k=3)

    # call qna service to get the answers
    return await completions.qna(
        question=question, context=[result.source for result in results]
    )
