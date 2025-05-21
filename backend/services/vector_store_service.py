import logging
import os
from typing import List, Optional, Union

import faiss
from langchain.docstore.document import Document
from langchain.retrievers import EnsembleRetriever
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS, Chroma

from core.config import settings
from core.factories.embeddings_factory import get_embeddings

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(self):
        self.embeddings = get_embeddings()
        self._initialize_store()

    def _initialize_store(self):
        # Clear existing store when changing providers
        if hasattr(self, "store"):
            del self.store

        if settings.vector_store.provider == "faiss":
            self.store = self._initialize_faiss()
        elif settings.vector_store.provider == "chroma":
            self.store = self._initialize_chroma()

    def as_retiever(self, **kwargs):
        return self.store.as_retriever(**kwargs)

    def save(self):
        os.makedirs(settings.paths.faiss_index_dir, exist_ok=True)
        self.store.save_local(settings.paths.faiss_index_dir)

    def get_document(self, document_id: str) -> Optional[Document]:
        try:
            docstore = self.store.docstore
            document = docstore.search(document_id)

            if isinstance(document, Document):
                return document
            return None
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {str(e)}")
            raise e

    def update_document(self, document_id: str, newDocument: Document) -> bool:
        try:
            if newDocument:
                newDocument.metadata["id"] = document_id
                self.delete_documents([document_id])
                self.add_documents([newDocument])
            return True
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {e}")
            raise e

    def get_documents(self) -> list[Document]:
        docstore = self.store.docstore
        index_to_docstore_id = self.store.index_to_docstore_id

        # Retrieve all documents
        all_documents = []
        for index, doc_id in index_to_docstore_id.items():
            document = docstore.search(doc_id)
            if document:
                all_documents.append(document)

        return all_documents

    def add_documents(self, documents: List[Document]) -> bool:
        try:
            for doc in documents:
                if self.chunk_in_store(doc.id):
                    print(f"Document {doc.id} already in store")
                    return False
                else:
                    print(f"Document {doc.id} already in store")
                    return False
            self.store.add_documents(documents)
            self.save()
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise e

    def _initialize_chroma(self, documents=None):
        logging.info("Initializing empty Chroma vector store with hello world")
        store = Chroma.from_documents(
            documents=documents or [Document(page_content="hello world")],
            embedding=self.embeddings,
            allow_dangerous_deserialization=True,
        )
        store.save_local(settings.paths.faiss_index_dir)
        return store

    def _initialize_faiss(self):
        try:
            # Try to get dimension from HuggingFace embeddings
            if hasattr(self.embeddings, "client") and hasattr(
                self.embeddings.client, "dimension"
            ):
                embedding_dim = self.embeddings.client.dimension
            elif hasattr(self.embeddings, "model") and hasattr(
                self.embeddings.model, "config"
            ):
                embedding_dim = self.embeddings.model.config.hidden_size
            else:
                # Fallback for other embedding types: compute dimension from a test embedding
                embedding_dim = len(self.embeddings.embed_query("test"))

            logger.info(f"Using embedding dimension: {embedding_dim}")
        except Exception as e:
            logger.error(f"Error determining embedding dimension: {e}")
            # Fallback to computing dimension
            embedding_dim = len(self.embeddings.embed_query("test"))
            logger.info(
                f"Fallback: Using computed embedding dimension: {embedding_dim}"
            )

        if (
            os.path.exists(settings.paths.faiss_index_dir)
            and len(os.listdir(settings.paths.faiss_index_dir)) > 0
        ):
            logging.info("Loading existing FAISS vector store")
            store = FAISS.load_local(
                settings.paths.faiss_index_dir,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            # Verify dimension match
            if store.index.d != embedding_dim:
                raise ValueError(
                    f"Embedding dimension mismatch: Index has {store.index.d}D vs Model has {embedding_dim}D"
                )
        else:
            logging.info(f"Initializing new FAISS index with dimension {embedding_dim}")
            index = faiss.IndexFlatL2(embedding_dim)
            store = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
            store.save_local(settings.paths.faiss_index_dir)
        return store

    def chunk_in_store(self, chunk_id: str) -> bool:
        index_to_docstore_id = self.store.index_to_docstore_id
        return chunk_id in index_to_docstore_id.values()
