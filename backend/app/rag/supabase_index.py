from llama_index.core import Document
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.storage import StorageContext
from llama_index.vector_stores.supabase import SupabaseVectorStore

from app.config import settings

vector_store = SupabaseVectorStore(
    postgres_connection_string=(settings.SUPABASE_DB_CONNECTION),
    collection_name="demo",
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context
)
query_engine = index.as_query_engine()

parser = MarkdownNodeParser()


def insert_document(text: str) -> None:
    # create the document
    doc = Document(text=text)

    # parse the article as nodes
    nodes = parser.get_nodes_from_documents([doc])

    # insert the nodes
    index.insert_nodes(nodes)
    index.storage_context.persist()


async def query(q: str) -> RESPONSE_TYPE:
    return await query_engine.aquery(q)
