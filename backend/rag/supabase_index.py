# pretty the output
from rich import pretty, print

pretty.install()


# debug mode
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from os import getenv

from llama_index.core import Document
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.storage import StorageContext
from llama_index.vector_stores.supabase import SupabaseVectorStore

host = "aws-0-ap-northeast-1.pooler.supabase.com"
port = 6543
db_name = "postgres"
user = "postgres.ntbquwgxdpmatqarupon"
password = getenv("SUPABASE_PASSWORD")


vector_store = SupabaseVectorStore(
    postgres_connection_string=(
        f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    ),
    collection_name="base_demo",
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
