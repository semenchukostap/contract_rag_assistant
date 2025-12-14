"""Tests for prompts module."""

from core.prompts import QA_PROMPT, NER_PROMPT, get_enhanced_qa_prompt


def test_qa_prompt_contains_required_placeholders():
    """Test that QA_PROMPT contains required placeholders."""
    assert "{context}" in QA_PROMPT
    assert "{input}" in QA_PROMPT


def test_ner_prompt_contains_required_placeholder():
    """Test that NER_PROMPT contains required placeholder."""
    assert "{contract_text}" in NER_PROMPT


def test_get_enhanced_qa_prompt_no_feedback():
    """Test get_enhanced_qa_prompt returns base prompt when no feedback."""
    assert get_enhanced_qa_prompt(None) == QA_PROMPT
    assert get_enhanced_qa_prompt([]) == QA_PROMPT


def test_get_enhanced_qa_prompt_with_positive_feedback():
    """Test get_enhanced_qa_prompt with positive feedback examples."""
    feedback = [
        {"rating": "up", "question": "Q1", "answer": "A1"},
        {"rating": "up", "question": "Q2", "answer": "A2"},
    ]

    result = get_enhanced_qa_prompt(feedback)

    assert "Learning from Previous Interactions" in result
    assert "Examples of helpful answers" in result
    assert "Q1" in result
    assert "Q2" in result


def test_get_enhanced_qa_prompt_with_negative_feedback():
    """Test get_enhanced_qa_prompt with negative feedback examples."""
    feedback = [{"rating": "down", "question": "Q1", "answer": "A1", "comment": "Incomplete"}]

    result = get_enhanced_qa_prompt(feedback)

    assert "Examples to avoid" in result
    assert "Incomplete" in result


def test_get_enhanced_qa_prompt_limits_examples():
    """Test that get_enhanced_qa_prompt limits number of examples."""
    feedback = [{"rating": "up", "question": f"Q{i}", "answer": f"A{i}"} for i in range(10)]

    result = get_enhanced_qa_prompt(feedback)

    assert "Q0" in result
    assert "Q1" in result
    assert result.count("Question:") <= 4  # 2 positive + potentially 2 negative
