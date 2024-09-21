from contextlib import asynccontextmanager

import app.storages.document as storages
from app.routers import context, documents
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    await storages.initialize()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(documents.router)
app.include_router(context.router)
