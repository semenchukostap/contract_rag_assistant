"""Feedback mechanism for improving answers over multiple interactions.

This module handles collecting, storing, and retrieving user feedback
to improve the contract QA system's responses.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from config.settings import FEEDBACK_FILE_PATH


def save_feedback(
    question: str,
    answer: str,
    rating: str,
    comment: Optional[str] = None,
    sources: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Save user feedback to a JSONL file.

    Args:
        question: The question that was asked.
        answer: The answer that was provided.
        rating: User rating - "up" for positive, "down" for negative.
        comment: Optional comment from the user.
        sources: Optional list of source documents used in the answer.

    Raises:
        RuntimeError: If feedback cannot be saved to file.
    """
    feedback_entry: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "answer": answer,
        "rating": rating,
    }

    if comment:
        feedback_entry["comment"] = comment

    if sources:
        feedback_entry["sources"] = [{"page": src.get("page", "Unknown")} for src in sources]

    feedback_path = Path(FEEDBACK_FILE_PATH)
    feedback_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(feedback_path, "a+", encoding="utf-8") as f:
            f.write(json.dumps(feedback_entry) + "\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        raise RuntimeError(f"Failed to save feedback to {feedback_path}: {str(e)}") from e


def clear_all_feedback() -> None:
    """Clear all feedback entries from the feedback file.

    Raises:
        RuntimeError: If feedback file cannot be deleted.
    """
    feedback_path = Path(FEEDBACK_FILE_PATH)
    if feedback_path.exists():
        try:
            feedback_path.unlink()
        except Exception as e:
            raise RuntimeError(f"Failed to clear feedback file: {str(e)}") from e


def load_feedback(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Load feedback history from the JSONL file.

    Args:
        limit: Optional limit on number of feedback entries to return.

    Returns:
        List of feedback dictionaries, most recent first.
    """
    feedback_path = Path(FEEDBACK_FILE_PATH)
    if not feedback_path.exists():
        return []

    feedback_entries = []
    try:
        with open(feedback_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        feedback_entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        # Skip malformed lines
                        continue
    except OSError:
        # File may be locked or inaccessible, return empty list
        return []

    feedback_entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return feedback_entries[:limit] if limit else feedback_entries


def get_feedback_stats() -> Dict[str, int]:
    """Get statistics about feedback collected.

    Returns:
        Dictionary with feedback statistics including total count,
        positive/negative counts.
    """
    try:
        feedback_entries = load_feedback()
    except (OSError, json.JSONDecodeError):
        return {"total": 0, "positive": 0, "negative": 0}

    return {
        "total": len(feedback_entries),
        "positive": sum(1 for entry in feedback_entries if entry.get("rating") == "up"),
        "negative": sum(1 for entry in feedback_entries if entry.get("rating") == "down"),
    }


def get_feedback_for_question(question: str) -> List[Dict[str, Any]]:
    """Get feedback entries for a specific question (or similar questions).

    Args:
        question: The question to search for.

    Returns:
        List of feedback entries related to the question.
    """
    all_feedback = load_feedback()
    question_lower = question.lower().strip()

    return [
        entry
        for entry in all_feedback
        if question_lower == entry.get("question", "").lower().strip()
        or question_lower in entry.get("question", "").lower().strip()
    ]
