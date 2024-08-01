from pydantic import BaseModel


class Embedding(BaseModel):
    source: str
    embedding: list[float]
