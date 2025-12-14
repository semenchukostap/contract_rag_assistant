"""Named Entity Recognition module for extracting key contract entities."""

import json
from typing import Dict, List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.settings import LLM_MODEL, OPENAI_API_KEY
from core.prompts import NER_PROMPT


def extract_entities(contract_text: str) -> Dict[str, Optional[str | List[str]]]:
    """
    Extract key entities from contract text using LLM.

    Extracts structured information including parties, dates, payment terms,
    IP ownership, and governing law from the provided contract text.

    Args:
        contract_text: Full text content of the contract.

    Returns:
        Dictionary containing extracted entities with the following keys:
        - parties: List of party names (list of strings)
        - effective_date: Effective date in YYYY-MM-DD format or null
        - termination_date: Termination date in YYYY-MM-DD format or null
        - payment_terms: Payment terms description or null
        - ip_owner: IP owner information or null
        - governing_law: Governing law/jurisdiction or null

    Raises:
        ValueError: If contract_text is empty.
        RuntimeError: If OPENAI_API_KEY is not set.
        ValueError: If the LLM response cannot be parsed as valid JSON.
    """
    if not contract_text or not contract_text.strip():
        raise ValueError("Contract text cannot be empty")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required for entity extraction")

    # Initialize LLM
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    # Create prompt template from NER_PROMPT
    prompt = ChatPromptTemplate.from_template(NER_PROMPT)

    # Create chain
    chain = prompt | llm

    # Invoke the chain
    response = chain.invoke({"contract_text": contract_text})

    # Extract content from response
    content = response.content
    if isinstance(content, list):
        response_text = "\n".join(str(item) for item in content)
    else:
        response_text = content
    response_text = response_text.strip()

    # Parse JSON response
    try:
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        entities = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse LLM response as JSON: {e}. Response: {response_text[:200]}"
        )

    # Validate and normalize the response structure
    expected_keys = {
        "parties",
        "effective_date",
        "termination_date",
        "payment_terms",
        "ip_owner",
        "governing_law",
    }

    # Ensure all expected keys are present
    result: Dict[str, Optional[str | List[str]]] = {}
    for key in expected_keys:
        result[key] = entities.get(key)

    return result
