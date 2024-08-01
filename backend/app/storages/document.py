from .client import supabase

bucket_id: str = "demo"


try:
    supabase.storage.get_bucket(bucket_id)
except:
    supabase.storage.create_bucket(
        id=bucket_id,
        options={
            "allowed_mime_types": ["text/plain", "text/markdown"],
            "file_size_limit": 1024 * 1024,
        },
    )


def upload_document(*, file: bytes, path: str):
    supabase.storage.from_(bucket_id).upload(file=file, path=path)
