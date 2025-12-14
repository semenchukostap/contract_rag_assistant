# Contract RAG Assistant

A RAG-based question answering system for contract documents using LangChain, FAISS, and OpenAI.

## Features

- Upload PDF contracts and ask questions
- Named Entity Recognition (NER) for key contract information
- Feedback mechanism to improve answers over time
- Source document citations with page numbers

## Setup

### Prerequisites

- Python 3.10 or higher (tested with 3.13)
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation

1. **Install uv** (if not already installed):

   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Or with pip
   pip install uv
   ```

2. **Install dependencies**:

   ```bash
   # uv sync automatically creates .venv and installs all dependencies from uv.lock
   # No need to create .venv manually!
   uv sync

   # Install with dev dependencies (pytest, ruff, etc.)
   uv sync --extra dev
   ```

3. **Configure environment**:

   Create a [`.env`](.env) file in the project root:

   ```env
   OPENAI_API_KEY=your_api_key_here
   LLM_MODEL=gpt-4o-mini
   EMBEDDING_MODEL=text-embedding-3-small
   ```

## Running the Application

### Start the Streamlit App

```bash
# Using uv (recommended - automatically uses .venv)
uv run streamlit run app.py

# Or activate the virtual environment manually
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
streamlit run app.py
```

> **Note:** The main application file is [app.py](app.py), which orchestrates the UI components and services. The application follows a clean architecture with separated concerns: UI rendering in `ui/`, business logic in `core/`, and service orchestration in `services/`.

The application will open in your browser at `http://localhost:8501`.

### Usage

1. Upload a PDF contract using the sidebar (E.g. [sample_contract.pdf](data/sample_contract.pdf))
2. Wait for the contract to be processed (text extraction, entity extraction, vector store creation)
3. Ask questions about the contract using the input field or quick questions
4. View answers with source citations
5. Provide feedback to improve future answers

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_feedback.py
# Or: uv run pytest tests/test_chunking.py, tests/test_embeddings.py, etc.

# Run with coverage
uv run pytest --cov=core --cov=config --cov=services --cov=ui

# Or activate venv first
source .venv/bin/activate
pytest
```

### Test Structure

- [conftest.py](tests/conftest.py) - Shared fixtures for all tests
- [test_chunking.py](tests/test_chunking.py) - Tests for document chunking
- [test_feedback.py](tests/test_feedback.py) - Tests for feedback mechanism
- [test_embeddings.py](tests/test_embeddings.py) - Tests for embeddings module
- [test_vectorstore.py](tests/test_vectorstore.py) - Tests for vector store operations
- [test_prompts.py](tests/test_prompts.py) - Tests for prompt templates
- [test_ingest.py](tests/test_ingest.py) - Tests for PDF ingestion
- [test_qa.py](tests/test_qa.py) - Tests for question answering
- [test_ner.py](tests/test_ner.py) - Tests for named entity recognition
- [test_services.py](tests/test_services.py) - Tests for service layer modules

### Test Best Practices

- Each test is independent and can run in isolation
- External dependencies (API calls, file I/O) are mocked
- Tests use fixtures for setup and teardown
- Tests follow the Arrange-Act-Assert pattern

## Development

### Code Quality

```bash
# Lint with ruff
uv run ruff check .

# Format with ruff
uv run ruff format .
```

### Managing Dependencies

```bash
# Update lock file after changing pyproject.toml
uv lock
# See [pyproject.toml](pyproject.toml) for dependency definitions

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Update all dependencies to latest compatible versions
uv lock --upgrade

# Check for outdated packages
uv pip list --outdated
```

### Troubleshooting

**Clear cache and reinstall:**

```bash
rm -rf .venv
uv sync
```

**Check installed packages:**

```bash
uv pip list
```

**Verify lock file is up to date:**

```bash
uv lock --check
```

## Project Structure

- [app.py](app.py) - Streamlit application entry point (orchestrates UI and services)
- [config/](config/) - Configuration settings
  - [settings.py](config/settings.py) - Application configuration and environment variables
- [core/](core/) - Core application modules (business logic)
  - [chunking.py](core/chunking.py) - Document chunking
  - [embeddings.py](core/embeddings.py) - Embedding generation
  - [feedback.py](core/feedback.py) - Feedback management
  - [ingest.py](core/ingest.py) - PDF ingestion
  - [ner.py](core/ner.py) - Named Entity Recognition
  - [prompts.py](core/prompts.py) - Prompt templates
  - [qa.py](core/qa.py) - Question answering
  - [vectorstore.py](core/vectorstore.py) - Vector store management
- [services/](services/) - Service layer (business logic orchestration)
  - [pdf_service.py](services/pdf_service.py) - PDF processing service
  - [qa_service.py](services/qa_service.py) - Question answering service
- [ui/](ui/) - UI components (Streamlit rendering)
  - [components.py](ui/components.py) - UI rendering components
  - [feedback.py](ui/feedback.py) - Feedback UI handling
  - [session_state.py](ui/session_state.py) - Session state management
- [tests/](tests/) - Test suite
- [data/](data/) - Data directory (PDFs, indices, feedback)
- [pyproject.toml](pyproject.toml) - Project configuration and dependencies
- [uv.lock](uv.lock) - Locked dependencies (generated by uv)
