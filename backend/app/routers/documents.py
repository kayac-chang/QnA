import io
import uuid
from typing import Annotated

from fastapi import APIRouter, File, Path, UploadFile

import app.storages.document as storages

DocumentId = Annotated[str, Path(description="The id of the document")]
DocumentContent = Annotated[
    UploadFile, File(description="The document which the user wants to upload")
]


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post("/")
async def upload_document(document: DocumentContent):
    """
    Upload a document
    """

    content = await document.read()

    storages.upload_document(file=content, path=document.filename or str(uuid.uuid4()))

    return "ok"


@router.get("/")
def get_documents():
    """
    Get all documents
    """
    ...


@router.get("/{document_id}")
def get_document(document_id: DocumentId):
    """
    Get the document by document id
    """
    ...


@router.put("/{document_id}")
def edit_document(document_id: DocumentId, document: DocumentContent):
    """
    Edit the document by document id
    """
    ...


@router.delete("/{document_id}")
def delete_document(document_id: DocumentId):
    """
    Delete the document by document id
    """
    ...
