from fastapi import FastAPI

from app.graph import graph

from app.schemas import (
    QuestionRequest,
    QuestionResponse,
)

app = FastAPI(
    title="Zepto Support Assistant",
    version="1.0.0",
)


@app.get("/")
def health():

    return {

        "status": "running"

    }


@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask_question(
    request: QuestionRequest,
):

    result = graph.invoke(

        {

            "question":
                request.query

        }

    )

    response = QuestionResponse(

        answer=result["answer"],

        sources=result["sources"],

        confidence=result["confidence"],

    )

    return response