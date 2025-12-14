"""UI components for rendering different sections of the app."""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

import streamlit as st

from config.settings import (
    ANSWER_PREVIEW_LENGTH,
    ENTITY_LABELS,
    FEEDBACK_HISTORY_LIMIT,
    MAX_SOURCES,
    PREFILLED_QUESTIONS,
    QUICK_QUESTIONS_COLS,
    SOURCE_CONTENT_PREVIEW_LENGTH,
)
from core.feedback import get_feedback_stats, load_feedback


def display_entities(entities: Dict[str, Optional[str | List[str]]]) -> None:
    """Display extracted contract entities in a table."""
    table_data = []
    for key, label in ENTITY_LABELS.items():
        value = entities.get(key)
        if value:
            display_value = (
                ", ".join(value) if key == "parties" and isinstance(value, list) else str(value)
            )
        else:
            display_value = "Not found"
        table_data.append({"Entity": label, "Value": display_value})
    st.dataframe(table_data, width="stretch", hide_index=True)


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp for display."""
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return timestamp[:19] if len(timestamp) > 19 else timestamp


def render_feedback_history() -> None:
    """Render feedback history in an expander."""
    feedback_entries = load_feedback(limit=FEEDBACK_HISTORY_LIMIT)
    if not feedback_entries:
        st.info("No feedback entries yet.")
        return

    st.caption(f"Showing {len(feedback_entries)} most recent entries")
    for entry in feedback_entries:
        rating_emoji = "👍" if entry.get("rating") == "up" else "👎"
        st.markdown(f"**{rating_emoji} {format_timestamp(entry.get('timestamp', ''))}**")
        st.markdown(f"**Q:** {entry.get('question', 'N/A')}")
        st.markdown(f"**A:** {entry.get('answer', 'N/A')[:ANSWER_PREVIEW_LENGTH]}...")
        if entry.get("comment"):
            st.markdown(f"*Comment:* {entry.get('comment')}")
        st.divider()


def render_feedback_stats() -> None:
    """Render feedback statistics section in sidebar."""
    try:
        feedback_stats = get_feedback_stats()
        st.divider()
        st.header("📊 Feedback Statistics")

        if feedback_stats["total"] > 0:
            st.metric("Total Feedback", feedback_stats["total"])
            col_pos, col_neg = st.columns(2)
            with col_pos:
                st.metric("👍 Positive", feedback_stats["positive"])
            with col_neg:
                st.metric("👎 Negative", feedback_stats["negative"])
            with st.expander("📋 View Feedback History", expanded=False):
                render_feedback_history()
        else:
            st.info("No feedback yet. Provide feedback on answers to see statistics here.")
    except Exception as e:
        st.warning(f"⚠️ Could not load feedback statistics: {str(e)}")


def render_quick_questions() -> None:
    """Render quick questions section."""
    st.subheader("💡 Quick Questions")
    st.markdown("Click a question below to use it:")

    for i in range(0, len(PREFILLED_QUESTIONS), QUICK_QUESTIONS_COLS):
        cols = st.columns(QUICK_QUESTIONS_COLS)
        for j, col in enumerate(cols):
            if i + j < len(PREFILLED_QUESTIONS):
                with col:
                    if st.button(
                        PREFILLED_QUESTIONS[i + j], key=f"question_{i + j}", width="stretch"
                    ):
                        st.session_state.question_input = PREFILLED_QUESTIONS[i + j]
                        st.rerun()


def render_question_input() -> Tuple[str, bool]:
    """Render question input field and button.

    Returns:
        Tuple of (question text, send_button clicked).
    """
    st.markdown("**Ask a question about the contract:**")
    col_question, col_button = st.columns([5, 1], gap="small")

    with col_question:
        question = st.text_input(
            "Ask a question about the contract:",
            placeholder="e.g., What is the termination clause?",
            help="Enter your question about the contract or select from quick questions above",
            key="question_input",
            label_visibility="collapsed",
        )

    with col_button:
        send_button = st.button("Ask", type="primary", width="stretch", key="send_question")

    return question, send_button


def render_answer_and_sources(answer: str, sources: List[Dict[str, str]]) -> None:
    """Render answer and source documents."""
    st.subheader("💡 Answer")
    st.write(answer)

    if sources:
        st.subheader("📄 Source Documents")
        for i, source in enumerate(sources[:MAX_SOURCES], 1):
            with st.expander(f"Source {i} - Page {source['page']}"):
                content = source["content"]
                display_content = (
                    content[:SOURCE_CONTENT_PREVIEW_LENGTH] + "..."
                    if len(content) > SOURCE_CONTENT_PREVIEW_LENGTH
                    else content
                )
                st.text(display_content)


def render_sidebar() -> None:
    """Render sidebar with PDF upload and feedback statistics."""
    from core.feedback import clear_all_feedback
    from services.pdf_service import process_pdf

    with st.sidebar:
        st.header("📤 Upload Contract")
        uploaded_file = st.file_uploader(
            "Choose a PDF file", type=["pdf"], help="Upload a PDF contract to analyze"
        )

        if uploaded_file is not None:
            if st.button("Process PDF", type="primary"):
                try:
                    clear_all_feedback()
                except RuntimeError:
                    # Feedback file may not exist, continue
                    pass

                vectorstore = process_pdf(uploaded_file)
                if vectorstore:
                    st.session_state.vectorstore = vectorstore
                    st.success(
                        f"✅ PDF processed successfully! ({vectorstore.index.ntotal} chunks indexed)"
                    )
                else:
                    st.session_state.vectorstore = None

        render_feedback_stats()
