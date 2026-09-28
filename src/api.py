from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.rag_pipeline import RAGPipeline


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Enterprise Knowledge Search API",
    description="Hybrid RAG API for enterprise document search.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# RAG PIPELINE
# ============================================================

pipeline = RAGPipeline()


# ============================================================
# REQUEST MODELS
# ============================================================

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Natural-language question to ask the knowledge repository.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of evidence chunks to retrieve.",
    )


# ============================================================
# RESPONSE HELPERS
# ============================================================

def format_source(item: dict[str, Any]) -> dict[str, Any]:
    """
    Convert an internal RAG evidence item into a clean API response.
    """

    return {
        "document_id": item.get("document"),
        "chunk_id": item.get("chunk_id"),
        "page": item.get("page"),
        "chunk_number": item.get("chunk_number"),
        "score": item.get("score"),
        "text": item.get("text"),
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    """
    Basic API health check.
    """

    return {
        "status": "ok",
        "service": "enterprise-knowledge-search",
        "rag_pipeline": "ready",
    }


# ============================================================
# QUERY
# ============================================================

@app.post("/query")
def query(request: QueryRequest):
    """
    Ask a question against the enterprise knowledge repository.
    """

    try:

        result = pipeline.ask(
            question=request.question,
            top_k=request.top_k,
        )

        return {
            "success": True,
            "question": result["question"],
            "answer": result["answer"],
            "abstained": result["abstained"],
            "sources": [
                format_source(item)
                for item in result["retrieved_evidence"]
            ],
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "service": "enterprise-knowledge-search",
        "status": "running",
        "docs": "/docs",
    }