"""Vector store module for building and managing FAISS vector stores."""

from pathlib import Path
from typing import List, Union

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from config.settings import FAISS_INDEX_PATH
from core.embeddings import get_embeddings


def build_vectorstore(documents: List[Document]) -> FAISS:
    """Build a FAISS vector store from a list of chunked Document objects.

    Creates embeddings for the documents and builds a FAISS index for
    efficient similarity search.

    Args:
        documents: List of chunked LangChain Document objects.

    Returns:
        FAISS vector store instance.

    Raises:
        ValueError: If documents list is empty.
    """
    if not documents:
        raise ValueError("Cannot build vector store from an empty list of documents")

    embeddings = get_embeddings()
    return FAISS.from_documents(documents=documents, embedding=embeddings)


def save_vectorstore(vectorstore: FAISS, path: Union[str, Path, None] = None) -> None:
    """Save a FAISS vector store to disk.

    Args:
        vectorstore: FAISS vector store instance to save.
        path: Optional path to save the vector store. If not provided,
              uses FAISS_INDEX_PATH from settings.
    """
    if path is None:
        path = FAISS_INDEX_PATH

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(path))
