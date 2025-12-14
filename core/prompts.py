"""Prompt templates for the contract QA system.

This module contains all prompt definitions used throughout the application.
Prompts are defined as string constants to keep them separate from business logic.
"""

from typing import Any, Dict, List, Optional

# QA prompt for Retrieval-Augmented Generation (RAG)
QA_PROMPT: str = """You are a legal contract assistant. Your task is to answer questions about a contract based solely on the provided context.

Context from the contract:
{context}

Question: {input}

Instructions:
1. Answer the question using ONLY the information provided in the context above.
2. Do not use any knowledge outside of the provided context.
3. Do not make up or infer information that is not explicitly stated in the context.
4. If the answer to the question cannot be found in the provided context, respond with exactly: "Not found in the contract"
5. When referencing information from the contract, include the page number(s) from the source documents in your answer (e.g., "According to page 3..." or "As stated on pages 5-6...").

Answer:"""

# NER prompt for extracting key contract entities
NER_PROMPT: str = """You are a legal contract analysis assistant. Extract key entities from the following contract text.

Contract text:
{contract_text}

Extract the following entities and return them as a JSON object with these exact keys:
- parties: List of party names (e.g., ["Company A", "Company B"])
- effective_date: The date when the contract becomes effective (format: YYYY-MM-DD or null if not found)
- termination_date: The date when the contract terminates or expires (format: YYYY-MM-DD or null if not found)
- payment_terms: Payment terms, amounts, and schedules (string or null if not found)
- ip_owner: Who owns the intellectual property (string or null if not found)
- governing_law: Which jurisdiction's law governs the contract (string or null if not found)

Instructions:
1. Extract information ONLY from the provided contract text.
2. Do not make up or infer information that is not explicitly stated.
3. If an entity is not found, use null for that field.
4. Return ONLY valid JSON, no additional text or explanation.
5. Dates should be in YYYY-MM-DD format if found, otherwise null.

Return the JSON object:"""

# Constants for feedback prompt enhancement
MAX_FEEDBACK_EXAMPLES = 2
EXAMPLE_ANSWER_PREVIEW_LENGTH = 200


def get_enhanced_qa_prompt(feedback_examples: Optional[List[Dict[str, Any]]] = None) -> str:
    """Get an enhanced QA prompt that incorporates feedback to improve answers.

    Args:
        feedback_examples: List of feedback dictionaries with previous interactions.

    Returns:
        Enhanced prompt string that includes feedback guidance.
    """
    if not feedback_examples:
        return QA_PROMPT

    positive_examples = [f for f in feedback_examples if f.get("rating") == "up"][
        :MAX_FEEDBACK_EXAMPLES
    ]
    negative_examples = [f for f in feedback_examples if f.get("rating") == "down"][
        :MAX_FEEDBACK_EXAMPLES
    ]

    feedback_guidance = "\n\n## Learning from Previous Interactions:\n"

    if positive_examples:
        feedback_guidance += "\n**Examples of helpful answers:**\n"
        for i, example in enumerate(positive_examples, 1):
            feedback_guidance += f"{i}. Question: {example.get('question', '')}\n"
            answer_preview = example.get("answer", "")[:EXAMPLE_ANSWER_PREVIEW_LENGTH]
            feedback_guidance += f"   Answer: {answer_preview}...\n"
        feedback_guidance += (
            "\nThese answers were rated as helpful. Use similar style and completeness.\n"
        )

    if negative_examples:
        feedback_guidance += "\n**Examples to avoid (these were rated as not helpful):**\n"
        for i, example in enumerate(negative_examples, 1):
            feedback_guidance += f"{i}. Question: {example.get('question', '')}\n"
            answer_preview = example.get("answer", "")[:EXAMPLE_ANSWER_PREVIEW_LENGTH]
            feedback_guidance += f"   Previous answer: {answer_preview}...\n"
            if example.get("comment"):
                feedback_guidance += f"   Issue: {example.get('comment')}\n"
        feedback_guidance += "\nAvoid these issues. Provide more complete and accurate answers.\n"

    return QA_PROMPT.replace("\nAnswer:", feedback_guidance + "\nAnswer:")
