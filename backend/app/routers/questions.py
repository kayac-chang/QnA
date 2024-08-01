from typing import Annotated

from fastapi import APIRouter, Form

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)


@router.post("/")
async def submit_question(query: Annotated[str, Form()]):
    """
    Submit one shot q&a
    """
    ...
