"""Streamlit application for contract question answering.

This module provides a web interface for uploading PDF contracts and asking
questions. It orchestrates calls to core modules without containing any RAG logic.
"""

import streamlit as st

from config.settings import MAX_SOURCES
from services.qa_service import process_question
from ui.components import (
    display_entities,
    render_answer_and_sources,
    render_question_input,
    render_quick_questions,
    render_sidebar,
)
from ui.feedback import render_feedback_section
from ui.session_state import initialize_session_state


def _process_question(question: str) -> None:
    """Process a question and display the answer."""
    if st.session_state.get("last_question") != question:
        st.session_state.feedback_submitted = False
        st.session_state.show_comment = False

    try:
        answer, sources, feedback_used = process_question(st.session_state.vectorstore, question)

        if feedback_used:
            st.info("💡 This answer was improved using feedback from previous interaction(s).")

        st.session_state.last_question = question
        st.session_state.last_answer = answer
        st.session_state.last_sources = sources[:MAX_SOURCES]

        render_answer_and_sources(answer, sources[:MAX_SOURCES])

    except ValueError as e:
        st.error(f"Invalid input: {str(e)}")
    except RuntimeError as e:
        st.error(f"Configuration error: {str(e)}")
    except Exception as e:
        st.error(f"Error answering question: {str(e)}")


def _render_main_content() -> None:
    """Render main content area with questions and answers."""
    if st.session_state.vectorstore is None:
        st.info("👈 Please upload a PDF contract in the sidebar to get started.")
        return

    if st.session_state.get("entities"):
        with st.expander("📋 Extracted Contract Entities", expanded=False):
            display_entities(st.session_state.entities)

    render_quick_questions()
    st.divider()

    question, send_button = render_question_input()

    if send_button and question:
        _process_question(question.strip())
    elif st.session_state.get("last_question") and st.session_state.get("show_comment"):
        render_answer_and_sources(
            st.session_state.get("last_answer", "No answer available"),
            st.session_state.get("last_sources", []),
        )

    render_feedback_section()


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(page_title="Contract QA Assistant", page_icon="📄", layout="wide")
    st.title("📄 Contract Question Answering Assistant")

    initialize_session_state()
    render_sidebar()
    _render_main_content()


if __name__ == "__main__":
    main()
