"""Tests for embeddings module."""

from core.embeddings import MockEmbeddings, get_embeddings


def test_mock_embeddings_init():
    """Test MockEmbeddings initialization."""
    embeddings = MockEmbeddings()
    assert embeddings.dimension == 1536


def test_mock_embeddings_custom_dimension():
    """Test MockEmbeddings with custom dimension."""
    embeddings = MockEmbeddings(dimension=512)
    assert embeddings.dimension == 512


def test_mock_embeddings_embed_documents():
    """Test MockEmbeddings embed_documents method."""
    embeddings = MockEmbeddings()
    texts = ["text1", "text2", "text3"]

    result = embeddings.embed_documents(texts)

    assert len(result) == 3
    assert all(len(vector) == 1536 for vector in result)
    assert all(all(val == 0.0 for val in vector) for vector in result)


def test_mock_embeddings_embed_query():
    """Test MockEmbeddings embed_query method."""
    embeddings = MockEmbeddings()
    result = embeddings.embed_query("test query")

    assert len(result) == 1536
    assert all(val == 0.0 for val in result)


def test_get_embeddings_without_api_key(monkeypatch):
    """Test get_embeddings returns MockEmbeddings when API key is not set."""
    monkeypatch.setattr("core.embeddings.OPENAI_API_KEY", "")
    embeddings = get_embeddings()
    assert isinstance(embeddings, MockEmbeddings)
