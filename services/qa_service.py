"""Service for handling question answering."""

from typing import Dict, List, Tuple

import streamlit as st
from langchain_community.vectorstores import FAISS

from core.feedback import get_feedback_for_question
from core.qa import answer_question


def process_question(vectorstore: FAISS, question: str) -> Tuple[str, List[Dict[str, str]], bool]:
    """Process a question and return answer with sources.

    Args:
        vectorstore: FAISS vector store containing documents.
        question: User's question.

    Returns:
        Tuple of (answer, sources, feedback_used).
    """
    related_feedback = get_feedback_for_question(question)
    feedback_used = len(related_feedback) > 0

    spinner_text = "Searching contract and generating answer..."
    if feedback_used:
        spinner_text += " (Using feedback to improve answer...)"

    with st.spinner(spinner_text):
        answer, sources = answer_question(vectorstore, question)

    return answer, sources, feedback_used
