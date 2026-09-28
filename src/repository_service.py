from datetime import datetime, timezone

from src.supabase_client import supabase


# ============================================================
# Repository Service
# ============================================================
#
# Handles document lifecycle operations:
#
#   Pending Approval
#          ↓
#       Approved
#          ↓
#        Routed
#
# This service is intentionally separate from FastAPI.
# FastAPI will call these functions later.
# ============================================================


DOCUMENT_TABLE = "documents"


# ------------------------------------------------------------
# Get all documents
# ------------------------------------------------------------

def get_documents(
    status=None,
    department=None,
    limit=100
):
    """
    Retrieve documents from the repository.

    Optional filters:
        status
        department
    """

    query = (
        supabase
        .table(DOCUMENT_TABLE)
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
    )

    if status:
        query = query.eq("status", status)

    if department:
        query = query.eq("department", department)

    response = query.execute()

    return response.data


# ------------------------------------------------------------
# Get one document
# ------------------------------------------------------------

def get_document(document_id):
    """
    Retrieve a single document by ID.
    """

    response = (
        supabase
        .table(DOCUMENT_TABLE)
        .select("*")
        .eq("id", document_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


# ------------------------------------------------------------
# Approve document
# ------------------------------------------------------------

def approve_document(document_id):
    """
    Approve a document.

    A document must exist before it can be approved.
    """

    document = get_document(document_id)

    if document is None:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    current_status = document.get("status")

    if current_status not in [
        "Pending Approval",
        "Pending"
    ]:
        raise ValueError(
            f"Document cannot be approved from status "
            f"'{current_status}'"
        )

    approved_at = datetime.now(
        timezone.utc
    ).isoformat()

    response = (
        supabase
        .table(DOCUMENT_TABLE)
        .update({
            "status": "Approved",
            "approved_at": approved_at
        })
        .eq("id", document_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Document approval failed."
        )

    return response.data[0]


# ------------------------------------------------------------
# Route document
# ------------------------------------------------------------

def route_document(
    document_id,
    routed_to
):
    """
    Route an approved document to a destination.

    Example destinations:
        Finance
        HR
        Legal
        Engineering
        Compliance
    """

    if not routed_to or not routed_to.strip():
        raise ValueError(
            "routed_to is required."
        )

    document = get_document(document_id)

    if document is None:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    current_status = document.get("status")

    if current_status != "Approved":
        raise ValueError(
            "Document must be approved before routing."
        )

    response = (
        supabase
        .table(DOCUMENT_TABLE)
        .update({
            "status": "Routed",
            "routed_to": routed_to.strip()
        })
        .eq("id", document_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Document routing failed."
        )

    return response.data[0]


# ------------------------------------------------------------
# Approve + Route
# ------------------------------------------------------------

def approve_and_route(
    document_id,
    routed_to
):
    """
    Convenience operation that performs:

        Pending Approval
              ↓
           Approved
              ↓
            Routed

    """

    approved_document = approve_document(
        document_id
    )

    routed_document = route_document(
        document_id,
        routed_to
    )

    return routed_document


# ------------------------------------------------------------
# Repository statistics
# ------------------------------------------------------------

def get_repository_stats():
    """
    Return basic repository statistics.
    """

    documents = get_documents(
        limit=1000
    )

    total = len(documents)

    pending = sum(
        1 for d in documents
        if d.get("status") == "Pending Approval"
    )

    approved = sum(
        1 for d in documents
        if d.get("status") == "Approved"
    )

    routed = sum(
        1 for d in documents
        if d.get("status") == "Routed"
    )

    return {
        "total": total,
        "pending_approval": pending,
        "approved": approved,
        "routed": routed
    }