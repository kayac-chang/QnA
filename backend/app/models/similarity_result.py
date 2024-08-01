from pydantic import BaseModel


class SimilarityResult(BaseModel):
    distance: float
    source: str
