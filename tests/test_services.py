"""Tests for service modules."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from services.qa_service import process_question


@pytest.fixture
def mock_vectorstore(mock_embeddings) -> FAISS:
    """Create a mock vectorstore for testing."""
    docs = [
        Document(page_content="Test content", metadata={"page": 1}),
    ]
    return FAISS.from_documents(docs, mock_embeddings)


@pytest.fixture
def mock_streamlit() -> Generator[MagicMock, None, None]:
    """Mock Streamlit for testing."""
    with patch("services.qa_service.st") as mock_st:
        mock_st.spinner.return_value.__enter__ = MagicMock()
        mock_st.spinner.return_value.__exit__ = MagicMock()
        yield mock_st


def test_process_question(mock_vectorstore, mock_streamlit, monkeypatch):
    """Test question processing."""
    # Mock answer_question to avoid API calls
    mock_answer = "Test answer"
    mock_sources = [{"content": "Test content", "page": 1}]

    with patch("services.qa_service.answer_question") as mock_answer_question:
        mock_answer_question.return_value = (mock_answer, mock_sources)

        with patch("services.qa_service.get_feedback_for_question") as mock_get_feedback:
            mock_get_feedback.return_value = []

            answer, sources, feedback_used = process_question(mock_vectorstore, "Test question?")

            assert answer == mock_answer
            assert sources == mock_sources
            assert feedback_used is False
            mock_answer_question.assert_called_once_with(mock_vectorstore, "Test question?")


def test_process_question_with_feedback(mock_vectorstore, mock_streamlit, monkeypatch):
    """Test question processing with feedback."""
    mock_answer = "Test answer"
    mock_sources = [{"content": "Test content", "page": 1}]
    mock_feedback = [{"rating": "up", "question": "Test question?"}]

    with patch("services.qa_service.answer_question") as mock_answer_question:
        mock_answer_question.return_value = (mock_answer, mock_sources)

        with patch("services.qa_service.get_feedback_for_question") as mock_get_feedback:
            mock_get_feedback.return_value = mock_feedback

            answer, sources, feedback_used = process_question(mock_vectorstore, "Test question?")

            assert answer == mock_answer
            assert sources == mock_sources
            assert feedback_used is True
            mock_get_feedback.assert_called_once_with("Test question?")
