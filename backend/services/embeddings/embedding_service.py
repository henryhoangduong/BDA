import logging
from typing import Dict, List, Optional, Union, cast

from langchain.schema import Document

from core.factories.database_factory import get_database
from core.factories.vector_store_factory import VectorStoreFactory
from models.simbadoc import SimbaDoc
from services.embeddings.utils import _clean_documents
from services.splitting.splitter import Splitter

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        """Initialize the EmbeddingService with necessary components."""
        self.vector_store = VectorStoreFactory.get_vector_store()
        self.database = get_database()
        self.splitter = Splitter(chunk_size=5000, chunk_overlap=300)

    def embed_all_documents(self) -> List[Document]:
        """
        Embed all documents in the database into the vector store.

        Returns:
            List of embedded langchain documents
        """
        try:
            # Get all documents from the database
            all_documents = self.database.get_all_documents()
            simba_documents = [cast(SimbaDoc, doc) for doc in all_documents]

            # Convert to Langchain documents
            langchain_documents = [
                doc for simbadoc in simba_documents for doc in simbadoc.documents
            ]

            # Clean documents
            langchain_documents = _clean_documents(langchain_documents)

            # Add documents to vector store
            self.vector_store.add_documents(langchain_documents)

            # Update enabled status for each document
            for doc in simba_documents:
                doc.metadata.enabled = True
                self.database.update_document(doc.id, doc)

            return langchain_documents
        except Exception as e:
            logger.error(f"Error embedding all documents: {str(e)}")
            raise

    def embed_document(self, doc_id: str) -> List[Document]:
        """
        Embed a specific document into the vector store.

        Args:
            doc_id: The ID of the document to embed

        Returns:
            List of embedded langchain documents
        """
        try:
            # Get document from database
            simbadoc: SimbaDoc = self.database.get_document(doc_id)
            if not simbadoc:
                raise ValueError(f"Document {doc_id} not found")

            langchain_documents = simbadoc.documents

            langchain_documents = self.splitter.split_document(langchain_documents)

            # Clean documents
            langchain_documents = _clean_documents(langchain_documents)

            try:
                # Add documents to vector store
                self.vector_store.add_documents(
                    document_id=doc_id, documents=langchain_documents
                )

                # Update document status
                simbadoc.metadata.enabled = True
                self.database.update_document(doc_id, simbadoc)

            except ValueError as ve:
                # If the error is about existing IDs, consider it a success
                if "Tried to add ids that already exist" in str(ve):
                    return langchain_documents
                raise ve  # Re-raise if it's a different ValueError

            return langchain_documents

        except Exception as e:
            logger.error(f"Error embedding document {doc_id}: {str(e)}")
            raise
