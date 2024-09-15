from contextlib import asynccontextmanager

from app.config import settings
from pydantic import BaseModel, Field, TypeAdapter
from supabase import acreate_client

bucket_id: str = "demo"


@asynccontextmanager
async def connection():
    """
    Get the Supabase async client
    """
    yield await acreate_client(
        supabase_url=settings.SUPABASE_API_URL,
        supabase_key=settings.SUPABASE_API_KEY,
    )


async def initialize():
    """
    Initialize the bucket
    """
    async with connection() as client:
        # Check if the bucket exists
        try:
            await client.storage.get_bucket(bucket_id)

        # If it doesn't exist, create it
        except:
            await client.storage.create_bucket(
                id=bucket_id,
                options={
                    "allowed_mime_types": ["text/plain", "text/markdown"],
                    "file_size_limit": 1024 * 1024,
                },
            )


async def upload(file: bytes, path: str, content_type: str):
    """
    Upload a file to the bucket
    """
    async with connection() as client:
        return await client.storage.from_(bucket_id).upload(
            file=file,
            path=path,
            file_options={"content-type": content_type, "upsert": "true"},
        )


class Metadata(BaseModel):
    eTag: str
    size: int
    mime_type: str = Field(validation_alias="mimetype")
    cache_control: str = Field(validation_alias="cacheControl")
    last_modified: str = Field(validation_alias="lastModified")
    content_length: int = Field(validation_alias="contentLength")
    http_status_code: int = Field(validation_alias="httpStatusCode")


class Folder(BaseModel):
    name: str


class File(BaseModel):
    id: str
    name: str
    updated_at: str
    created_at: str
    last_accessed_at: str
    metadata: Metadata


async def get_all(path: str | None = None) -> list[File]:
    """
    get all files in the bucket
    """
    async with connection() as client:
        res = await client.storage.from_(bucket_id).list(path)

        items = TypeAdapter(list[Folder | File]).validate_python(res)

        res = []
        for item in items:
            _path = f"{path}/{item.name}" if path else item.name

            match item:
                # Recursively list the folder
                case Folder():
                    res.extend(await get_all(_path))
                # Skip the placeholder file
                case File(name=".emptyFolderPlaceholder"):
                    continue
                # Add the file to the list
                case File():
                    item.name = _path
                    res.append(item)
        return res


async def delete(*path: str):
    async with connection() as client:
        return await client.storage.from_(bucket_id).remove([*path])


async def download(path: str) -> bytes:
    async with connection() as client:
        return await client.storage.from_(bucket_id).download(path)


async def get_url(path: str) -> str:
    async with connection() as client:
        return await client.storage.from_(bucket_id).get_public_url(path)
