"""Tests for vectorstore module."""

import pytest

from core.vectorstore import build_vectorstore, save_vectorstore


def test_build_vectorstore(monkeypatch, sample_documents, mock_embeddings):
    """Test building vectorstore from documents."""
    monkeypatch.setattr("core.vectorstore.get_embeddings", lambda: mock_embeddings)

    vectorstore = build_vectorstore(sample_documents)

    assert vectorstore is not None
    assert vectorstore.index.ntotal == len(sample_documents)


def test_build_vectorstore_empty_list(monkeypatch, mock_embeddings):
    """Test building vectorstore raises error for empty list."""
    monkeypatch.setattr("core.vectorstore.get_embeddings", lambda: mock_embeddings)
    with pytest.raises(ValueError, match="Cannot build vector store from an empty list"):
        build_vectorstore([])


def test_save_vectorstore(monkeypatch, temp_dir, sample_documents, mock_embeddings):
    """Test saving vectorstore to disk."""
    monkeypatch.setattr("core.vectorstore.get_embeddings", lambda: mock_embeddings)
    vectorstore = build_vectorstore(sample_documents)
    save_path = temp_dir / "test_index"

    save_vectorstore(vectorstore, path=save_path)

    assert save_path.exists()
    assert (save_path / "index.faiss").exists()
    assert (save_path / "index.pkl").exists()
