"""PDF ingestion module for extracting text from PDF files."""

from pathlib import Path
from typing import List, Union

import pdfplumber
from langchain_core.documents import Document


def load_pdf(pdf_path: Union[str, Path]) -> List[Document]:
    """Load a PDF file and extract text page by page.

    Extracts text from each page of the PDF and creates LangChain Document
    objects with page numbers in metadata. Handles empty or malformed pages
    gracefully by skipping them or including empty text.

    Args:
        pdf_path: Path to the PDF file to load.

    Returns:
        List of LangChain Document objects, each containing:
        - page_content: The extracted text from the page
        - metadata: Dictionary with 'page' key containing the page number (1-indexed)

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file is not a valid PDF.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    documents: List[Document] = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                try:
                    text = page.extract_text()

                    if text is None or text.strip() == "":
                        text = ""

                    doc = Document(page_content=text, metadata={"page": page_num})
                    documents.append(doc)

                except Exception as e:
                    doc = Document(page_content="", metadata={"page": page_num, "error": str(e)})
                    documents.append(doc)

    except Exception as e:
        raise ValueError(f"Failed to load PDF: {pdf_path}. Error: {e}") from e

    return documents
