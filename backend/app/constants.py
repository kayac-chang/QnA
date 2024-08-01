from typing import Literal, get_args

TYPE_SUPPORTED_EMBEDDING_MODEL = Literal[
    "text-embedding-ada-002", "text-embedding-3-small"
]
""" The supported embedding models """

SUPPOTED_EMBEDDING_MODEL: tuple[str] = get_args(TYPE_SUPPORTED_EMBEDDING_MODEL)

EMBEDDING_DIMENSIONS: dict[TYPE_SUPPORTED_EMBEDDING_MODEL, int] = {
    "text-embedding-ada-002": 1536,
    "text-embedding-3-small": 1536,
}
