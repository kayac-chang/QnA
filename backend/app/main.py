from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.storages.document as storages
from app.routers import context, documents, embeddings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await storages.initialize()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(documents.router)
app.include_router(embeddings.router)
app.include_router(context.router)
