import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel
from supabase import StorageException

import app.storages.document as storages


class Document(BaseModel):
    name: str
    updated_at: str
    created_at: str
    last_accessed_at: str
    size: int
    mimetype: str
    last_modified: str


class Error(BaseModel):
    detail: str


DocumentContent = Annotated[
    UploadFile, File(description="The document which the user wants to upload")
]


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


def embedding(document_name: str):
    ...
    # find the document by name

    # extract the content

    # send the content to the embedding service


@router.post(
    "/",
    responses={
        400: {"description": "Bad Request", "model": Error},
        201: {"description": "Success"},
        # 202: {"description": "Accepted"},
    },
)
async def upload_document(document: DocumentContent, tasks: BackgroundTasks) -> bool:
    """
    Upload a document
    """
    try:
        # if the filename is not provided, generate a random name
        path = document.filename or str(uuid.uuid4())

        # read the file content
        content = await document.read()

        # upload the document to the storage
        res = await storages.upload(
            file=content,
            path=path,
            content_type=document.headers["content-type"],
        )

        # send the document to the background task (embedding)
        # tasks.add_task(embedding, document_name=path)

        return res.is_success

    # handle the storage exception
    except StorageException as e:
        err = e.args[0]
        raise HTTPException(
            status_code=err["statusCode"],
            detail=err["message"],
        )


@router.get(
    "/",
    responses={
        200: {"description": "Success"},
    },
)
async def list_documents() -> list[Document]:
    """
    List all documents
    """
    return [
        Document(
            name=file.name,
            updated_at=file.updated_at,
            created_at=file.created_at,
            last_accessed_at=file.last_accessed_at,
            size=file.metadata.size,
            mimetype=file.metadata.mime_type,
            last_modified=file.metadata.last_modified,
        )
        for file in await storages.list()
    ]


@router.get(
    "/{document_name}",
    responses={
        404: {"description": "Document not found", "model": Error},
        200: {"description": "Success"},
    },
)
async def get_document(document_name: str) -> Document:
    """
    Get the document by name
    """
    docs = await list_documents()

    for doc in docs:
        if doc.name == document_name:
            return doc

    # raise an exception if the document is not found
    raise HTTPException(status_code=404, detail="document not found")


@router.get(
    "/{document_name}/content",
    responses={
        404: {"description": "Document not found", "model": Error},
        200: {"description": "Success"},
    },
)
async def get_document_content(document_name: str) -> Response:
    """
    Get the document content by name
    """
    # get the document by name
    doc = await get_document(document_name)

    # download the document content
    content = await storages.download(doc.name)

    # return the document content with the appropriate mimetype
    return Response(content=content, media_type=doc.mimetype)


@router.delete(
    "/{document_name}",
    responses={
        404: {"description": "Document not found", "model": Error},
        200: {"description": "Success"},
    },
)
async def delete_document(document_name: str) -> bool:
    """
    Delete the document by name
    """
    # get the document by name
    doc = await get_document(document_name)

    # delete the document from storages
    await storages.delete(doc.name)

    return True
