"""Tests for NER module."""

import pytest

from core.ner import extract_entities


def test_extract_entities_empty_text():
    """Test extract_entities raises error for empty text."""
    with pytest.raises(ValueError, match="Contract text cannot be empty"):
        extract_entities("")

    with pytest.raises(ValueError, match="Contract text cannot be empty"):
        extract_entities("   ")


def test_extract_entities_no_api_key(monkeypatch):
    """Test extract_entities raises error when API key is not set."""
    monkeypatch.setattr("core.ner.OPENAI_API_KEY", "")
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is required"):
        extract_entities("This is a contract between Company A and Company B.")
