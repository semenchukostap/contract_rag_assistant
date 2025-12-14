"""Question answering module for the contract QA system."""

from typing import Dict, List, Tuple

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI

from config.settings import LLM_MODEL, MAX_SOURCES, OPENAI_API_KEY
from core.feedback import get_feedback_for_question
from core.prompts import get_enhanced_qa_prompt


def answer_question(vectorstore: FAISS, question: str) -> Tuple[str, List[Dict[str, str]]]:
    """Answer a question about a contract using Retrieval-Augmented Generation.

    Uses the provided vector store to retrieve relevant context and generates
    an answer using the LLM with the custom QA prompt. Returns both the answer
    and source documents with page numbers.

    Args:
        vectorstore: FAISS vector store containing the contract documents.
        question: User's question about the contract.

    Returns:
        Tuple containing:
        - answer: The generated answer string
        - sources: List of dictionaries containing source document information
                   with 'page' key for page numbers and 'content' for text

    Raises:
        ValueError: If question is empty.
        RuntimeError: If OPENAI_API_KEY is not set (LLM requires API key).
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required for question answering")

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    related_feedback = get_feedback_for_question(question)
    enhanced_prompt = get_enhanced_qa_prompt(related_feedback)
    prompt = ChatPromptTemplate.from_template(enhanced_prompt)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever(search_kwargs={"k": MAX_SOURCES})
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    result = retrieval_chain.invoke({"input": question})

    sources = [
        {
            "content": doc.page_content,
            "page": doc.metadata.get("page", "Unknown"),
        }
        for doc in result["context"]
    ]

    return result["answer"], sources
