"""FastAPI entrypoint for the construction advisory backend.

This is a Phase 1 MVP: local-only, no auth, no payments, no database.
It loads approved knowledge from local Markdown files and uses a local
Ollama LLaMA model to draft a response in Alex's advisory style.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from knowledge_loader import load_knowledge_base
from retrieval import retrieve_relevant_entries
from llm import generate_answer

app = FastAPI(title="Construction Advisor API", version="0.1.0")


class ChatRequest(BaseModel):
    """Request body for /chat.

    Only `question` is required now. Optional `images` is reserved for future use.
    """

    question: str = Field(..., min_length=3)
    images: list[str] | None = None


class ChatResponse(BaseModel):
    """Response body for /chat."""

    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Generate an advisory response from local knowledge + LLaMA.

    Steps:
    1) Load approved Markdown knowledge.
    2) Retrieve the most relevant entries.
    3) Build a prompt that includes full sections and extra context notes.
    4) Call local Ollama LLaMA to generate a response.
    """

    try:
        knowledge_entries = load_knowledge_base()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if not knowledge_entries:
        raise HTTPException(
            status_code=500,
            detail="No approved knowledge entries found in knowledge/approved/."
        )

    relevant = retrieve_relevant_entries(request.question, knowledge_entries)

    answer = generate_answer(
        question=request.question,
        entries=relevant,
        image_refs=request.images or [],
    )

    return ChatResponse(answer=answer)
