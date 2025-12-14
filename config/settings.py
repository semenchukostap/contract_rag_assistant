"""Configuration settings for the contract QA project.

This module loads configuration from environment variables with sensible defaults.
All values can be overridden via a .env file or environment variables.
"""

import os
from typing import Dict, List

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# OpenAI configuration
# API key for OpenAI services (required for embeddings and LLM)
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# LLM model name for question answering
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Embedding model name for creating vector embeddings
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


# Text chunking configuration
# Size of each text chunk in characters
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "800"))

# Number of overlapping characters between consecutive chunks
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "150"))


# Vector store configuration
# Path where the FAISS vector store index will be saved and loaded from
FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "data/faiss_index")


# PDF processing configuration
# Temporary path for uploaded PDF files
PDF_TEMP_PATH: str = os.getenv("PDF_TEMP_PATH", "data/temp.pdf")

# Feedback configuration
# Path to the JSONL file where feedback is stored
FEEDBACK_FILE_PATH: str = os.getenv("FEEDBACK_FILE_PATH", "data/feedback.jsonl")

# UI configuration
# Maximum number of source documents to display
MAX_SOURCES: int = int(os.getenv("MAX_SOURCES", "3"))

# Number of feedback entries to show in history
FEEDBACK_HISTORY_LIMIT: int = int(os.getenv("FEEDBACK_HISTORY_LIMIT", "20"))

# Number of columns for quick questions display
QUICK_QUESTIONS_COLS: int = int(os.getenv("QUICK_QUESTIONS_COLS", "2"))

# Preview lengths for content display
SOURCE_CONTENT_PREVIEW_LENGTH: int = int(os.getenv("SOURCE_CONTENT_PREVIEW_LENGTH", "500"))
ANSWER_PREVIEW_LENGTH: int = int(os.getenv("ANSWER_PREVIEW_LENGTH", "150"))

# Prefilled questions for quick access
PREFILLED_QUESTIONS: List[str] = [
    "Who are the parties?",
    "What is the termination clause?",
    "What is the effective date of the contract?",
    "Who owns the intellectual property?",
    "Which law governs the contract?",
    "Who is Ostap?",
]

# Entity labels for display
ENTITY_LABELS: Dict[str, str] = {
    "parties": "👥 Parties",
    "effective_date": "📅 Effective Date",
    "termination_date": "📅 Termination Date",
    "payment_terms": "💰 Payment Terms",
    "ip_owner": "🔐 IP Owner",
    "governing_law": "⚖️ Governing Law",
}
