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


def ingest_document(
    file_bytes,
    filename
):
    """
    Complete ingestion flow.

    1. Validate and extract document
    2. Generate metadata
    3. Store original file in Supabase Storage
    4. Create document record in PostgreSQL
    5. Return document information

    The document remains Pending Approval until
    the Approve & Route workflow changes its status.
    """

    # --------------------------------------------------
    # 1. Extract document
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
    # 2. Generate metadata
    # --------------------------------------------------

    metadata = extract_metadata(
        filename,
        document_text
    )

    # --------------------------------------------------
    # 3. Create document ID
    # --------------------------------------------------

    document_id = str(
        uuid4()
    )

    extension = Path(
        filename
    ).suffix.lower()

    storage_path = (
        f"documents/{document_id}"
        f"/{filename}"
    )

    # --------------------------------------------------
    # 4. Store original document
    # --------------------------------------------------

    supabase.storage.from_(
        BUCKET_NAME
    ).upload(
        storage_path,
        file_bytes,
        {
            "content-type":
                get_content_type(extension),
            "upsert": "false"
        }
    )

    # --------------------------------------------------
    # 5. Create database record
    # --------------------------------------------------

    record = {
        "id": document_id,

        "filename": filename,

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
            len(file_bytes)
    }

    response = (
        supabase
        .table("documents")
        .insert(record)
        .execute()
    )

    if not response.data:

        raise RuntimeError(
            "Document was uploaded to Storage "
            "but the database record could not be created."
        )

    return {
        "success": True,
        "document_id": document_id,
        "filename": filename,
        "status": "Pending Approval",
        "metadata": metadata,
        "storage_path": storage_path
    }


def get_content_type(extension):

    content_types = {

        ".pdf":
            "application/pdf",

        ".txt":
            "text/plain",

        ".xlsx":
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        ".xlsm":
            "application/vnd.ms-excel.sheet.macroEnabled.12"
    }

    return content_types.get(
        extension,
        "application/octet-stream"
    )
