"""Tests for PDF ingestion module."""

import pytest

from core.ingest import load_pdf


def test_load_pdf_file_not_found():
    """Test load_pdf raises error for non-existent file."""
    with pytest.raises(FileNotFoundError, match="PDF file not found"):
        load_pdf("nonexistent_file.pdf")


def test_load_pdf_invalid_file(temp_dir):
    """Test load_pdf raises error for invalid PDF."""
    invalid_pdf = temp_dir / "invalid.pdf"
    invalid_pdf.write_text("This is not a PDF file")

    with pytest.raises(ValueError, match="Failed to load PDF"):
        load_pdf(invalid_pdf)
