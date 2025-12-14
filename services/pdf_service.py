"""Service for processing PDF files."""

from pathlib import Path
from typing import Optional

import streamlit as st
from langchain_community.vectorstores import FAISS

from config.settings import PDF_TEMP_PATH
from core.chunking import chunk_documents
from core.ingest import load_pdf
from core.ner import extract_entities
from core.vectorstore import build_vectorstore, save_vectorstore


def process_pdf(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> Optional[FAISS]:
    """Process an uploaded PDF file and create a vector store.

    Args:
        uploaded_file: Streamlit uploaded file object.

    Returns:
        FAISS vector store if successful, None otherwise.
    """
    temp_path = Path(PDF_TEMP_PATH)
    temp_path.parent.mkdir(parents=True, exist_ok=True)

    # Clean up existing temp file
    if temp_path.exists():
        try:
            temp_path.unlink()
        except OSError:
            # File may be locked or already deleted, continue
            pass

    try:
        # Save uploaded file
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text
        with st.spinner("Extracting text from PDF..."):
            documents = load_pdf(temp_path)

        if not documents:
            st.error("No text could be extracted from the PDF.")
            return None

        # Extract entities
        contract_text = "\n\n".join([doc.page_content for doc in documents])
        try:
            with st.spinner("Extracting contract entities..."):
                st.session_state.entities = extract_entities(contract_text)
        except RuntimeError:
            st.warning("⚠️ Entity extraction skipped (OPENAI_API_KEY not set)")
            st.session_state.entities = None
        except Exception as e:
            st.warning(f"⚠️ Entity extraction failed: {str(e)}")
            st.session_state.entities = None

        # Chunk documents
        with st.spinner("Chunking documents..."):
            chunks = chunk_documents(documents)

        # Build vector store
        with st.spinner("Creating embeddings and building vector store..."):
            vectorstore = build_vectorstore(chunks)

        save_vectorstore(vectorstore)
        return vectorstore

    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None
    finally:
        # Clean up temporary file
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                # File may be locked or already deleted, continue
                pass
