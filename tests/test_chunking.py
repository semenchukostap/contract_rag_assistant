"""Tests for chunking module."""

import pytest

from core.chunking import chunk_documents


def test_chunk_documents(sample_documents):
    """Test chunking of documents."""
    chunks = chunk_documents(sample_documents)

    assert len(chunks) > 0
    assert all(isinstance(chunk, type(sample_documents[0])) for chunk in chunks)
    assert any("page" in chunk.metadata for chunk in chunks)


def test_chunk_documents_empty_list():
    """Test chunking raises error for empty document list."""
    with pytest.raises(ValueError, match="Cannot chunk an empty list"):
        chunk_documents([])
