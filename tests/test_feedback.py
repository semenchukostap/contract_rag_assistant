"""Tests for feedback module."""

import json


from core.feedback import (
    clear_all_feedback,
    get_feedback_for_question,
    get_feedback_stats,
    load_feedback,
    save_feedback,
)


def test_save_feedback(mock_feedback_path):
    """Test saving feedback to file."""
    save_feedback(question="Test question?", answer="Test answer", rating="up")

    assert mock_feedback_path.exists()
    with open(mock_feedback_path) as f:
        entry = json.loads(f.readline().strip())
        assert entry["question"] == "Test question?"
        assert entry["answer"] == "Test answer"
        assert entry["rating"] == "up"


def test_save_feedback_with_comment(mock_feedback_path):
    """Test saving feedback with comment."""
    save_feedback(question="Test?", answer="Answer", rating="down", comment="Not helpful")

    with open(mock_feedback_path) as f:
        entry = json.loads(f.readline().strip())
        assert entry["comment"] == "Not helpful"


def test_save_feedback_with_sources(mock_feedback_path):
    """Test saving feedback with sources."""
    sources = [{"page": 1}, {"page": 2}]
    save_feedback(question="Test?", answer="Answer", rating="up", sources=sources)

    with open(mock_feedback_path) as f:
        entry = json.loads(f.readline().strip())
        assert len(entry["sources"]) == 2
        assert entry["sources"][0]["page"] == 1


def test_load_feedback_empty_file(mock_feedback_path):
    """Test loading feedback from non-existent file."""
    assert load_feedback() == []


def test_load_feedback_with_entries(mock_feedback_path):
    """Test loading feedback from file with entries."""
    entries = [
        {
            "timestamp": "2024-01-15T10:00:00+00:00",
            "question": "Q1",
            "answer": "A1",
            "rating": "up",
        },
        {
            "timestamp": "2024-01-16T10:00:00+00:00",
            "question": "Q2",
            "answer": "A2",
            "rating": "down",
        },
    ]

    with open(mock_feedback_path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    feedback = load_feedback()
    assert len(feedback) == 2
    assert feedback[0]["question"] == "Q2"  # Most recent first


def test_load_feedback_with_limit(mock_feedback_path):
    """Test loading feedback with limit."""
    with open(mock_feedback_path, "w") as f:
        for i in range(5):
            entry = {
                "timestamp": f"2024-01-{15 + i}T10:00:00+00:00",
                "question": f"Q{i}",
                "answer": f"A{i}",
                "rating": "up",
            }
            f.write(json.dumps(entry) + "\n")

    assert len(load_feedback(limit=2)) == 2


def test_clear_all_feedback(mock_feedback_path):
    """Test clearing all feedback."""
    mock_feedback_path.write_text("test content")
    assert mock_feedback_path.exists()

    clear_all_feedback()
    assert not mock_feedback_path.exists()


def test_clear_all_feedback_nonexistent(mock_feedback_path):
    """Test clearing feedback when file doesn't exist."""
    clear_all_feedback()
    assert not mock_feedback_path.exists()


def test_get_feedback_stats(mock_feedback_path):
    """Test getting feedback statistics."""
    entries = [
        {
            "timestamp": "2024-01-15T10:00:00+00:00",
            "question": "Q1",
            "answer": "A1",
            "rating": "up",
        },
        {
            "timestamp": "2024-01-16T10:00:00+00:00",
            "question": "Q2",
            "answer": "A2",
            "rating": "up",
        },
        {
            "timestamp": "2024-01-17T10:00:00+00:00",
            "question": "Q3",
            "answer": "A3",
            "rating": "down",
        },
    ]

    with open(mock_feedback_path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    stats = get_feedback_stats()
    assert stats == {"total": 3, "positive": 2, "negative": 1}


def test_get_feedback_stats_empty(mock_feedback_path):
    """Test getting feedback stats when no feedback exists."""
    assert get_feedback_stats() == {"total": 0, "positive": 0, "negative": 0}


def test_get_feedback_for_question(mock_feedback_path):
    """Test getting feedback for specific question."""
    entries = [
        {
            "timestamp": "2024-01-15T10:00:00+00:00",
            "question": "Who are the parties?",
            "answer": "A1",
            "rating": "up",
        },
        {
            "timestamp": "2024-01-16T10:00:00+00:00",
            "question": "What is the date?",
            "answer": "A2",
            "rating": "down",
        },
        {
            "timestamp": "2024-01-17T10:00:00+00:00",
            "question": "Who are the parties?",
            "answer": "A3",
            "rating": "up",
        },
    ]

    with open(mock_feedback_path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    feedback = get_feedback_for_question("Who are the parties?")
    assert len(feedback) == 2
    assert all(entry["question"] == "Who are the parties?" for entry in feedback)
