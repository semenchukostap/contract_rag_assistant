"""Session state management for Streamlit app."""

import streamlit as st

from core.feedback import clear_all_feedback


def initialize_session_state() -> None:
    """Initialize all session state variables."""
    defaults = {
        "vectorstore": None,
        "entities": None,
        "last_question": None,
        "last_answer": None,
        "last_sources": None,
        "feedback_submitted": False,
        "show_comment": False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

    if "app_initialized" not in st.session_state:
        try:
            clear_all_feedback()
        except RuntimeError:
            # Feedback file may not exist, continue
            pass
        st.session_state.app_initialized = True
