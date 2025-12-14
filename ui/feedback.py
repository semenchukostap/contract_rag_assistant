"""Feedback UI components."""

import traceback

import streamlit as st

from core.feedback import save_feedback


def handle_positive_feedback() -> None:
    """Handle positive feedback submission."""
    if not st.session_state.get("last_question") or not st.session_state.get("last_answer"):
        st.error("❌ Missing question or answer data. Please ask a question first.")
        return

    try:
        save_feedback(
            question=st.session_state.last_question,
            answer=st.session_state.last_answer,
            rating="up",
            sources=st.session_state.get("last_sources"),
        )
        st.session_state.feedback_submitted = True
        st.success(
            f"✅ Thank you for your positive feedback! It has been saved for: **{st.session_state.last_question}**"
        )
        st.rerun()
    except Exception as e:
        st.error(f"❌ Failed to save feedback: {str(e)}")
        with st.expander("Error Details"):
            st.code(traceback.format_exc())


def handle_negative_feedback(comment: str) -> None:
    """Handle negative feedback submission."""
    if not st.session_state.get("last_question") or not st.session_state.get("last_answer"):
        st.error("❌ Missing question or answer data. Please ask a question first.")
        return

    try:
        save_feedback(
            question=st.session_state.last_question,
            answer=st.session_state.last_answer,
            rating="down",
            comment=comment if comment.strip() else None,
            sources=st.session_state.get("last_sources"),
        )
        st.session_state.feedback_submitted = True
        st.session_state.show_comment = False
        st.success(
            f"✅ Thank you for your negative feedback! It has been saved for: **{st.session_state.last_question}**"
        )
        st.rerun()
    except Exception as e:
        st.error(f"❌ Failed to save feedback: {str(e)}")
        with st.expander("Error Details"):
            st.code(traceback.format_exc())


def render_feedback_section() -> None:
    """Render feedback section with buttons and comment field."""
    if not st.session_state.get("last_answer") or st.session_state.feedback_submitted:
        if st.session_state.get("last_answer") and st.session_state.feedback_submitted:
            st.divider()
            st.info("✅ Feedback submitted. Thank you!")
        return

    st.divider()
    st.subheader("📊 Feedback")
    st.markdown("Was this answer helpful? Your feedback helps improve the assistant.")
    st.caption(
        "💡 **How feedback improves answers:** When you provide feedback, the system learns from it. "
        "For similar questions in the future, it will use your previous feedback to provide better, "
        "more complete answers. Positive feedback helps identify good answer patterns, while negative "
        "feedback with comments helps avoid similar mistakes."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Helpful", width="stretch", type="primary", key="feedback_up"):
            handle_positive_feedback()
    with col2:
        if st.button("👎 Not Helpful", width="stretch", key="feedback_down"):
            st.session_state.show_comment = True
            st.rerun()

    if st.session_state.get("show_comment", False):
        if st.session_state.get("last_question"):
            st.info(f"📝 Reviewing feedback for: **{st.session_state.last_question}**")

        comment = st.text_area(
            "Please tell us how we can improve:",
            placeholder="e.g., The answer was incomplete, missing details about penalties.",
            key="feedback_comment",
        )

        col_submit, col_cancel = st.columns([1, 1])
        with col_submit:
            if st.button("Submit Feedback", type="primary", key="feedback_submit"):
                handle_negative_feedback(comment)
        with col_cancel:
            if st.button("Cancel"):
                st.session_state.show_comment = False
                st.rerun()
