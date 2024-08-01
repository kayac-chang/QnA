from fastapi import APIRouter

import app.constants as CONST
import app.services.embeddings as embeddings

router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"],
)


@router.get("/")
def get_supported_models() -> tuple[str]:
    return CONST.SUPPOTED_EMBEDDING_MODEL


@router.post("/{model_name}")
async def generate_embeddings(
    input: list[str],
    model_name: CONST.TYPE_SUPPORTED_EMBEDDING_MODEL = "text-embedding-ada-002",
) -> list[embeddings.Embedding]:
    """
    Send the content to the embedding service and generate the embeddings
    """
    return await embeddings.generate(input, model=model_name)
