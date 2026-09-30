from pathlib import Path
from uuid import uuid4

from src.document_processor import (
    extract_document,
    combine_document_text
)

from src.metadata_extractor import (
    extract_metadata
)

from src.supabase_client import (
    supabase,
    BUCKET_NAME
)


# --------------------------------------------------
# Upload rules
# --------------------------------------------------

MAX_FILE_SIZE = 3 * 1024 * 1024  # 3 MB

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".xlsx",
    ".txt"
}


# --------------------------------------------------
# Main ingestion function
# --------------------------------------------------

def ingest_document(
    file_bytes,
    filename
):
    """
    Complete document ingestion flow.

    Flow:

    1. Validate file type
    2. Validate file size
    3. Extract document content
    4. Generate AI metadata
    5. Store original file in Supabase Storage
    6. Create document record in PostgreSQL
    7. Leave document in Pending Approval state

    The document is NOT chunked, embedded, or indexed
    until it passes the human approval/routing workflow.
    """

    # --------------------------------------------------
    # 0. Validate filename
    # --------------------------------------------------

    if not filename:

        raise ValueError(
            "A filename is required."
        )

    extension = Path(
        filename
    ).suffix.lower()

    # --------------------------------------------------
    # 1. Validate file type
    # --------------------------------------------------

    if extension not in ALLOWED_EXTENSIONS:

        allowed = ", ".join(
            sorted(ALLOWED_EXTENSIONS)
        )

        raise ValueError(
            f"Unsupported file type '{extension}'. "
            f"Supported formats: {allowed}"
        )

    # --------------------------------------------------
    # 2. Validate file size
    # --------------------------------------------------

    file_size = len(file_bytes)

    if file_size == 0:

        raise ValueError(
            "The uploaded file is empty."
        )

    if file_size > MAX_FILE_SIZE:

        raise ValueError(
            "File size exceeds the 3 MB limit."
        )

    # --------------------------------------------------
    # 3. Extract document
    # --------------------------------------------------

    pages = extract_document(
        file_bytes,
        filename
    )

    if not pages:

        raise ValueError(
            "No readable content was found "
            "in the uploaded document."
        )

    document_text = combine_document_text(
        pages
    )

    if not document_text.strip():

        raise ValueError(
            "The uploaded document contains "
            "no readable text."
        )

    # --------------------------------------------------
    # 4. Generate metadata
    # --------------------------------------------------

    metadata = extract_metadata(
        filename,
        document_text
    )

    # --------------------------------------------------
    # 5. Create document ID
    # --------------------------------------------------

    document_id = str(
        uuid4()
    )

    storage_path = (
        f"documents/{document_id}"
        f"/{filename}"
    )

    # --------------------------------------------------
    # 6. Store original document
    # --------------------------------------------------

    supabase.storage.from_(
        BUCKET_NAME
    ).upload(
        storage_path,
        file_bytes,
        {
            "content-type":
                get_content_type(extension),

            "upsert":
                "false"
        }
    )

    # --------------------------------------------------
    # 7. Create database record
    # --------------------------------------------------

    record = {

        "id":
            document_id,

        "filename":
            filename,

        "title":
            metadata.get(
                "title"
            ),

        "department":
            metadata.get(
                "department",
                "General"
            ),

        "sensitivity":
            metadata.get(
                "sensitivity",
                "Internal"
            ),

        "tags":
            metadata.get(
                "tags",
                []
            ),

        "summary":
            metadata.get(
                "summary"
            ),

        "status":
            "Pending Approval",

        "storage_path":
            storage_path,

        "file_size_bytes":
            file_size
    }

    response = (
        supabase
        .table("documents")
        .insert(record)
        .execute()
    )

    # --------------------------------------------------
    # 8. Verify database record
    # --------------------------------------------------

    if not response.data:

        raise RuntimeError(
            "Document was uploaded to Storage "
            "but the database record could not be created."
        )

    # --------------------------------------------------
    # 9. Return ingestion result
    # --------------------------------------------------

    return {

        "success":
            True,

        "document_id":
            document_id,

        "filename":
            filename,

        "status":
            "Pending Approval",

        "metadata":
            metadata,

        "storage_path":
            storage_path,

        "file_size_bytes":
            file_size
    }


# --------------------------------------------------
# Content type helper
# --------------------------------------------------

def get_content_type(extension):

    content_types = {

        ".pdf":
            "application/pdf",

        ".docx":
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

        ".txt":
            "text/plain",

        ".xlsx":
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }

    return content_types.get(
        extension,
        "application/octet-stream"
    )