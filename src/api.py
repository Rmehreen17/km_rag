from typing import Any, Optional

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.rag_pipeline import RAGPipeline

from src.ingestion_service import (
    ingest_document,
)

from src.repository_service import (
    get_documents,
    get_document,
    approve_document,
    route_document,
    approve_and_route,
    get_repository_stats,
)

from src.indexing_service import (
    index_document,
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# RAG PIPELINE
# ============================================================

print("Initializing RAG pipeline...")

pipeline = RAGPipeline()

print("RAG pipeline ready.")


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
        description=(
            "Number of evidence chunks to retrieve."
        ),
    )


class RouteRequest(BaseModel):

    routed_to: str = Field(
        ...,
        min_length=1,
        description=(
            "Repository destination such as "
            "Finance, HR, Legal, Engineering or Compliance."
        ),
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

    return {
        "status": "ok",
        "service": "enterprise-knowledge-search",
        "rag_pipeline": "ready",
    }


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


# ============================================================
# RAG QUERY
# ============================================================


@app.post("/query")
def query(
    request: QueryRequest
):
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
                for item in result[
                    "retrieved_evidence"
                ]
            ],
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# INGEST DOCUMENT
# ============================================================


@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...)
):
    """
    Upload a document into the ingestion pipeline.

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
        Extract
          ↓
        Generate metadata
          ↓
        Store document
          ↓
        Pending Approval
    """

    try:

        # ----------------------------------------------------
        # Validate filename
        # ----------------------------------------------------

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="Filename is required.",
            )

        filename = file.filename

        # ----------------------------------------------------
        # Validate extension
        # ----------------------------------------------------

        allowed_extensions = {
            ".pdf",
            ".txt",
            ".xlsx",
            ".xlsm",
        }

        from pathlib import Path

        extension = (
            Path(filename)
            .suffix
            .lower()
        )

        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Please upload PDF, TXT, XLSX, or XLSM."
                ),
            )

        # ----------------------------------------------------
        # Read file
        # ----------------------------------------------------

        file_bytes = await file.read()

        if not file_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        # ----------------------------------------------------
        # Ingest
        # ----------------------------------------------------

        result = ingest_document(
            file_bytes=file_bytes,
            filename=filename,
        )

        return {
            "success": True,
            "message": (
                "Document uploaded successfully "
                "and is pending approval."
            ),
            "result": result,
        }

    except HTTPException:
        raise

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
# LIST DOCUMENTS
# ============================================================


@app.get("/documents")
def list_documents(
    status: Optional[str] = Query(
        default=None,
        description="Filter by document status.",
    ),
    department: Optional[str] = Query(
        default=None,
        description="Filter by department.",
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
    ),
):
    """
    Retrieve documents from the repository.

    Optional filters:

        status
        department
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
# GET SINGLE DOCUMENT
# ============================================================


@app.get("/documents/{document_id}")
def get_single_document(
    document_id: str
):
    """
    Retrieve a single document.
    """

    try:

        document = get_document(
            document_id
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail=(
                    f"Document not found: "
                    f"{document_id}"
                ),
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
# APPROVE DOCUMENT
# ============================================================


@app.post("/documents/{document_id}/approve")
def approve(
    document_id: str
):
    """
    Approve a document after human review.

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
# ROUTE DOCUMENT
# ============================================================


@app.post("/documents/{document_id}/route")
def route(
    document_id: str,
    request: RouteRequest,
):
    """
    Route an approved document
    to a repository destination.
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
# APPROVE + ROUTE
# ============================================================


@app.post(
    "/documents/{document_id}/approve-and-route"
)
def approve_and_route_document(
    document_id: str,
    request: RouteRequest,
):
    """
    Perform:

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
# INDEX DOCUMENT
# ============================================================


@app.post("/documents/{document_id}/index")
def index(
    document_id: str
):
    """
    Index an approved/routed document.

    Flow:

        Repository document
                ↓
        Download original file
                ↓
        Extract content
                ↓
        Create chunks
                ↓
        Generate embeddings
                ↓
        Store chunks + embeddings
                ↓
        Mark indexed
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
# REPOSITORY STATISTICS
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