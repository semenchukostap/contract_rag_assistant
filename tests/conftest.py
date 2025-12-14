"""Shared pytest fixtures for all tests."""

from pathlib import Path
from typing import Generator, List

import pytest
from langchain_core.documents import Document


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_documents() -> List[Document]:
    """Create sample documents for testing."""
    return [
        Document(
            page_content="This is a sample contract between Company A and Company B.",
            metadata={"page": 1},
        ),
        Document(
            page_content="The effective date is 2024-01-15. Payment terms are $10,000 per month.",
            metadata={"page": 2},
        ),
        Document(
            page_content=(
                "Intellectual property is owned by Company A. "
                "This contract is governed by California law."
            ),
            metadata={"page": 3},
        ),
    ]


@pytest.fixture
def mock_feedback_file(temp_dir: Path) -> Path:
    """Create a temporary feedback file."""
    return temp_dir / "test_feedback.jsonl"


@pytest.fixture
def mock_feedback_path(
    mock_feedback_file: Path, monkeypatch: pytest.MonkeyPatch
) -> Generator[Path, None, None]:
    """Fixture to set up mock feedback file path for all feedback tests."""
    import config.settings
    import core.feedback

    original_path = config.settings.FEEDBACK_FILE_PATH
    monkeypatch.setattr(config.settings, "FEEDBACK_FILE_PATH", str(mock_feedback_file))
    monkeypatch.setattr(core.feedback, "FEEDBACK_FILE_PATH", str(mock_feedback_file))

    yield mock_feedback_file

    config.settings.FEEDBACK_FILE_PATH = original_path


@pytest.fixture
def mock_embeddings():
    """Fixture providing MockEmbeddings instance."""
    from core.embeddings import MockEmbeddings

    return MockEmbeddings()
