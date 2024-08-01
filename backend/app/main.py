from fastapi import FastAPI

from .routers import documents, questions

app = FastAPI()

app.include_router(documents.router)
app.include_router(questions.router)
