"""
LangGraph workflow for the Zepto Support Assistant.
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from pydantic import ValidationError

from app.config import MOCK_LLM
from app.prompts import build_rag_prompt
from app.retrieval import retrieve_context
from app.schemas import QuestionResponse


class GraphState(TypedDict):
    question: str
    intent: str
    context: str
    answer: str
    confidence: float
    sources: list[str]


def validate_response(answer, sources, confidence):

    return QuestionResponse(
        answer=answer,
        sources=sources,
        confidence=confidence,
    )


# =====================================================
# classify_intent
# =====================================================

def classify_intent(state: GraphState):

    question = state["question"].lower()

    if MOCK_LLM:

        keywords = [
            "delivery",
            "return",
            "refund",
            "membership",
            "tracking",
            "cancel",
            "gift card",
            "support hours",
        ]

        intent = "general_question"

        if any(keyword in question for keyword in keywords):
            intent = "policy_question"

        return {"intent": intent}

    # Optional real LLM implementation
    return {"intent": "policy_question"}


# =====================================================
# retrieve_and_answer
# =====================================================

def retrieve_and_answer(state: GraphState):

    question = state["question"]

    documents, metadata, chunk_ids = retrieve_context(question)

    context = "\n\n".join(documents)

    if MOCK_LLM:

        snippet = documents[0][:200] if documents else ""

        validated = validate_response(
            answer=f"Based on the retrieved context: {snippet}",
            sources=chunk_ids,
            confidence=1.0,
        )

        return {
            "context": context,
            **validated.model_dump(),
        }

    # ------------------------------
    # Optional LLM implementation
    # ------------------------------

    prompt = build_rag_prompt(
        question,
        context,
    )

    retries = 3

    for _ in range(retries):

        raw_answer = prompt

        try:

            validated = validate_response(
                answer=raw_answer,
                sources=chunk_ids,
                confidence=0.95,
            )

            return {
                "context": context,
                **validated.model_dump(),
            }

        except ValidationError:

            prompt += (
                "\n\nReturn valid JSON only."
            )

    return {

        "context": context,

        "answer":
            "ERROR: Unable to generate a valid response.",

        "sources": [],

        "confidence": 0.0,
    }


# =====================================================
# direct_answer
# =====================================================

def direct_answer(state: GraphState):

    if MOCK_LLM:

        validated = validate_response(
            answer="I can only answer questions about Zepto policies right now.",
            sources=[],
            confidence=1.0,
        )

        return validated.model_dump()

    # Optional real LLM

    retries = 3

    prompt = state["question"]

    for _ in range(retries):

        raw_answer = prompt

        try:

            validated = validate_response(
                answer=raw_answer,
                sources=[],
                confidence=0.95,
            )

            return validated.model_dump()

        except ValidationError:

            prompt += (
                "\nReturn valid JSON only."
            )

    return {

        "answer":
            "ERROR: Unable to generate a valid response.",

        "sources": [],

        "confidence": 0.0,
    }


# =====================================================
# Router
# =====================================================

def route_question(state: GraphState):

    if state["intent"] == "policy_question":
        return "retrieve"

    return "direct"


# =====================================================
# Build Graph
# =====================================================

builder = StateGraph(GraphState)

builder.add_node(
    "classify",
    classify_intent,
)

builder.add_node(
    "retrieve",
    retrieve_and_answer,
)

builder.add_node(
    "direct",
    direct_answer,
)

builder.add_edge(
    START,
    "classify",
)

builder.add_conditional_edges(
    "classify",
    route_question,
    {
        "retrieve": "retrieve",
        "direct": "direct",
    },
)

builder.add_edge(
    "retrieve",
    END,
)

builder.add_edge(
    "direct",
    END,
)

graph = builder.compile()


if __name__ == "__main__":

    result = graph.invoke(
        {
            "question": "How do I track my delivery?"
        }
    )

    print(result)

    print()

    result = graph.invoke(
        {
            "question": "Who won IPL?"
        }
    )

    print(result)