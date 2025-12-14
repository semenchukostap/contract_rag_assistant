"""Embeddings module for creating vector embeddings from documents."""

from typing import List

from langchain_core.embeddings import Embeddings

from config.settings import OPENAI_API_KEY, EMBEDDING_MODEL


class MockEmbeddings(Embeddings):
    """Mock embeddings class for use when OpenAI API key is not available.

    Generates deterministic zero vectors for all inputs. Useful for testing
    and development when API access is not available.
    """

    def __init__(self, dimension: int = 1536) -> None:
        """Initialize mock embeddings.

        Args:
            dimension: Dimension of the embedding vectors (default: 1536,
                       matching OpenAI's text-embedding-3-small).
        """
        self.dimension = dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings for a list of documents.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of zero vectors (all zeros) with the specified dimension.
        """
        return [[0.0] * self.dimension for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        """Generate a mock embedding for a query.

        Args:
            text: Query text string to embed.

        Returns:
            Zero vector with the specified dimension.
        """
        return [0.0] * self.dimension


def get_embeddings() -> Embeddings:
    """Get an embeddings instance, using OpenAI if available, otherwise mock.

    Checks if OPENAI_API_KEY is set. If available, returns OpenAIEmbeddings.
    Otherwise, returns MockEmbeddings for fallback functionality.

    Returns:
        Embeddings instance (OpenAIEmbeddings or MockEmbeddings).
    """
    if OPENAI_API_KEY:
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return MockEmbeddings()
