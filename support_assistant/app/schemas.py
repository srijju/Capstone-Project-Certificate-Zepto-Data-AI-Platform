"""
Pydantic schemas for the Zepto Support Assistant.
"""

from typing import List

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Incoming request body.
    """

    query: str = Field(
        ...,
        description="User query",
        examples=["How do I track my delivery?"],
    )


class QuestionResponse(BaseModel):
    """
    Outgoing API response.
    """

    answer: str = Field(
        ...,
        description="Generated answer",
    )

    sources: List[str] = Field(
        default_factory=list,
        description="Retrieved chunk IDs.",
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score (0-1).",
    )


class AssistantResponse(BaseModel):
    """
    Internal response model.
    """

    answer: str
    sources: List[str]
    confidence: float