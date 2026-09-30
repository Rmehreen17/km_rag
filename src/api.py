from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.rag_pipeline import RAGPipeline
from src.ingestion_service import ingest_document
from src.indexing_service import index_document

from src.repository_service import (
    get_documents,
    get_document,
    approve_document,
    route_document,
    approve_and_route,
    get_repository_stats,
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Enterprise Knowledge Search API",
    description="Hybrid RAG API for enterprise document search.",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# RAG PIPELINE
# ============================================================

pipeline = RAGPipeline()


# ============================================================
# INGESTION CONFIGURATION
# ============================================================

MAX_FILE_SIZE = 3 * 1024 * 1024  # 3 MB

# These must match the current document_processor.py
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".xlsx",
    ".xlsm",
}


# ============================================================
# REQUEST MODELS
# ============================================================

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description=(
            "Natural-language question to ask "
            "the knowledge repository."
        ),
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of evidence chunks to retrieve.",
    )


class RouteRequest(BaseModel):
    routed_to: str = Field(
        ...,
        min_length=1,
        description="Repository destination for the document.",
    )


# ============================================================
# RESPONSE HELPERS
# ============================================================

def format_source(
    item: dict[str, Any]
) -> dict[str, Any]:
    """
    Convert an internal RAG evidence item
    into a clean API response.
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
    Ask a question against the enterprise
    knowledge repository.
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
# DOCUMENT INGESTION
# ============================================================

@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...)
):
    """
    Upload and ingest a document.

    Supported formats:

        PDF
        TXT
        XLSX
        XLSM

    Maximum file size:

        3 MB

    Flow:

        Upload
            ↓
        Validate
            ↓
        Extract text
            ↓
        Generate metadata
            ↓
        Store original document
            ↓
        Create repository record
            ↓
        Pending Approval
    """

    # --------------------------------------------------------
    # 1. Validate filename
    # --------------------------------------------------------

    filename = file.filename or ""

    if not filename:

        raise HTTPException(
            status_code=400,
            detail="A filename is required.",
        )

    # --------------------------------------------------------
    # 2. Validate extension
    # --------------------------------------------------------

    extension = Path(
        filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported formats: "
                "PDF, TXT, XLSX, XLSM."
            ),
        )

    # --------------------------------------------------------
    # 3. Read uploaded file
    # --------------------------------------------------------

    try:

        file_bytes = await file.read()

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unable to read uploaded file: "
                f"{str(exc)}"
            ),
        )

    # --------------------------------------------------------
    # 4. Validate empty file
    # --------------------------------------------------------

    if len(file_bytes) == 0:

        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # --------------------------------------------------------
    # 5. Validate file size
    # --------------------------------------------------------

    if len(file_bytes) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail=(
                "File exceeds the maximum allowed "
                "size of 3 MB."
            ),
        )

    # --------------------------------------------------------
    # 6. Run ingestion service
    # --------------------------------------------------------

    try:

        result = ingest_document(
            file_bytes=file_bytes,
            filename=filename,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# DOCUMENT INDEXING
# ============================================================

@app.post("/documents/{document_id}/index")
def index(
    document_id: str,
):
    """
    Index an approved or routed document
    into the RAG knowledge repository.

    Flow:

        Approved / Routed
              ↓
        Download document
              ↓
        Extract content
              ↓
        Create chunks
              ↓
        Generate embeddings
              ↓
        Store chunks
              ↓
        Update indexing status
    """

    try:

        result = index_document(
            document_id
        )

        return {
            "success": True,
            "message": "Document indexed successfully.",
            "result": result,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# REPOSITORY - LIST DOCUMENTS
# ============================================================

@app.get("/documents")
def list_documents(
    status: str | None = None,
    department: str | None = None,
    limit: int = 100,
):
    """
    Retrieve documents from the repository.

    Optional filters:

        status
        department
        limit
    """

    try:

        documents = get_documents(
            status=status,
            department=department,
            limit=limit,
        )

        return {
            "success": True,
            "documents": documents,
            "count": len(documents),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# REPOSITORY - GET DOCUMENT
# ============================================================

@app.get("/documents/{document_id}")
def get_document_by_id(
    document_id: str,
):
    """
    Retrieve a single document from the repository.
    """

    try:

        document = get_document(
            document_id
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        return {
            "success": True,
            "document": document,
        }

    except HTTPException:

        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# REPOSITORY - APPROVE
# ============================================================

@app.post("/documents/{document_id}/approve")
def approve(
    document_id: str,
):
    """
    Approve a document after human review.

    Lifecycle:

        Pending Approval
              ↓
           Approved
    """

    try:

        document = approve_document(
            document_id
        )

        return {
            "success": True,
            "message": "Document approved successfully.",
            "document": document,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# REPOSITORY - ROUTE
# ============================================================

@app.post("/documents/{document_id}/route")
def route(
    document_id: str,
    request: RouteRequest,
):
    """
    Route an approved document.

    Lifecycle:

        Approved
            ↓
         Routed
    """

    try:

        document = route_document(
            document_id=document_id,
            routed_to=request.routed_to,
        )

        return {
            "success": True,
            "message": "Document routed successfully.",
            "document": document,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# REPOSITORY - APPROVE + ROUTE
# ============================================================

@app.post(
    "/documents/{document_id}/approve-and-route"
)
def approve_and_route_document(
    document_id: str,
    request: RouteRequest,
):
    """
    Approve and route a document.

    Lifecycle:

        Pending Approval
              ↓
           Approved
              ↓
            Routed
    """

    try:

        document = approve_and_route(
            document_id=document_id,
            routed_to=request.routed_to,
        )

        return {
            "success": True,
            "message": (
                "Document approved and routed successfully."
            ),
            "document": document,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# REPOSITORY - STATISTICS
# ============================================================

@app.get("/repository/stats")
def repository_stats():
    """
    Return repository statistics.
    """

    try:

        stats = get_repository_stats()

        return {
            "success": True,
            "stats": stats,
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