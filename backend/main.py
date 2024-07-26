import uuid
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

app = FastAPI()


# @todo in-memory document database, should have id, name, and file src
class Document(BaseModel):
    id: str
    name: str
    src: str


documents: list[Document] = []

F = Annotated[
    UploadFile, File(description="The document which the user wants to upload")
]


@app.post("/documents", tags=["documents"])
def upload_document(document: F):
    """
    Upload a document
    """

    doc = Document(
        id=str(len(documents) + 1),
        name=document.filename or str(uuid.uuid4()),
        src="path/to/file",
    )

    documents.append(doc)

    return {"data": doc}


@app.get("/documents", tags=["documents"])
def get_documents():
    """
    Get all documents
    """
    return {"data": documents}


@app.get("/documents/{document_id}", tags=["documents"])
def get_document(document_id: str):
    """
    Get the document by document id
    """
    doc = next((doc for doc in documents if doc.id == document_id), None)
    if not doc:
        return {"error": "Document not found"}
    return {"data": doc}


@app.put("/documents/{document_id}", tags=["documents"])
def edit_document(document_id: str, document: F):
    """
    Edit the document by document id
    """
    doc = next((doc for doc in documents if doc.id == document_id), None)
    if not doc:
        return {"error": "Document not found"}
    return {"data": doc}


@app.delete("/documents/{document_id}", tags=["documents"])
def delete_document(document_id: str):
    """
    Delete the document by document id
    """
    doc = next((doc for doc in documents if doc.id == document_id), None)
    if not doc:
        return {"error": "Document not found"}
    documents.remove(doc)
    return {"data": "ok"}


@app.post("/questions", tags=["questions"])
def submit_question(query: str = Form(...)):
    """
    Submit one shot q&a
    """
    return {"answer": f"answer {query}"}
