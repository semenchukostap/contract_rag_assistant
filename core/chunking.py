"""Text chunking module for splitting documents into smaller pieces."""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split a list of LangChain Document objects into smaller chunks.

    Uses RecursiveCharacterTextSplitter to split documents into chunks of
    configurable size with configurable overlap. Preserves metadata from
    the original documents in each chunk.

    Args:
        documents: List of LangChain Document objects to chunk.

    Returns:
        List of chunked LangChain Document objects. Each chunk retains
        the metadata from its source document.

    Raises:
        ValueError: If documents list is empty.
    """
    if not documents:
        raise ValueError("Cannot chunk an empty list of documents")

    # Initialize the text splitter with settings from config
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # Split all documents into chunks
    chunked_documents = text_splitter.split_documents(documents)

    return chunked_documents
