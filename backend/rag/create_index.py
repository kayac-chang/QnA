import os

from llama_index.core.indices.base import BaseIndex

PERSIST_DIR = "./storage"


def create_vector_index_from_text(text: str) -> BaseIndex:
    if not os.path.exists(PERSIST_DIR):
        from llama_index.core.indices import VectorStoreIndex
        from llama_index.core.node_parser import MarkdownNodeParser
        from llama_index.core.schema import Document

        # create the document
        doc = Document(text=text)

        # parse the article as nodes
        parser = MarkdownNodeParser()
        nodes = parser.get_nodes_from_documents([doc])

        # create the index
        index = VectorStoreIndex(nodes)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        from llama_index.core import load_index_from_storage
        from llama_index.core.storage import StorageContext

        # restore the index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)

        # create the index
        index = load_index_from_storage(storage_context)

    return index
