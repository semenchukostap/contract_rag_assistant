"""Tests for question answering module."""

import pytest
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from core.qa import answer_question


def test_answer_question_empty_question(mock_embeddings):
    """Test answer_question raises error for empty question."""
    docs = [Document(page_content="test", metadata={"page": 1})]
    vectorstore = FAISS.from_documents(docs, mock_embeddings)

    with pytest.raises(ValueError, match="Question cannot be empty"):
        answer_question(vectorstore, "")

    with pytest.raises(ValueError, match="Question cannot be empty"):
        answer_question(vectorstore, "   ")


def test_answer_question_no_api_key(monkeypatch, mock_embeddings):
    """Test answer_question raises error when API key is not set."""

    monkeypatch.setattr("core.qa.OPENAI_API_KEY", "")
    docs = [Document(page_content="test", metadata={"page": 1})]
    vectorstore = FAISS.from_documents(docs, mock_embeddings)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is required"):
        answer_question(vectorstore, "test question")
