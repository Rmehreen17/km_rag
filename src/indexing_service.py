import json
from datetime import datetime, timezone

import numpy as np
from sentence_transformers import SentenceTransformer

from src.supabase_client import supabase
from src.document_processor import extract_document
from src.chunk_documents import create_chunks


# ============================================================
# Configuration
# ============================================================

BUCKET_NAME = "documents"

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# Load once when the service starts
print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model ready.")


# ============================================================
# Get document
# ============================================================

def get_document(document_id):

    response = (
        supabase
        .table("documents")
        .select("*")
        .eq("id", document_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise ValueError(
            f"Document not found: {document_id}"
        )

    return response.data[0]


# ============================================================
# Download original document
# ============================================================

def download_document(storage_path):

    response = (
        supabase
        .storage
        .from_(BUCKET_NAME)
        .download(storage_path)
    )

    if not response:
        raise ValueError(
            f"Could not download document: {storage_path}"
        )

    return response


# ============================================================
# Build chunks
# ============================================================

def build_document_chunks(
    document_id,
    filename,
    file_bytes
):

    pages = extract_document(
        file_bytes,
        filename
    )

    chunks = []

    for page in pages:

        page_number = page["page"]

        page_chunks = create_chunks(
            page["text"]
        )

        for chunk_number, chunk_text in enumerate(
            page_chunks,
            start=1
        ):

            chunk_id = (
                f"{document_id}"
                f"-P{page_number}"
                f"-C{chunk_number}"
            )

            chunks.append({
                "document_id": document_id,
                "chunk_id": chunk_id,
                "page": str(page_number),
                "chunk_number": chunk_number,
                "content": chunk_text
            })

    return chunks


# ============================================================
# Generate embeddings
# ============================================================

def generate_embeddings(chunks):

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    if not texts:
        return chunks

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        chunk["embedding"] = (
            np.asarray(embedding)
            .tolist()
        )

    return chunks


# ============================================================
# Save chunks
# ============================================================

def save_chunks(chunks):

    if not chunks:
        return 0

    rows = []

    for chunk in chunks:

        rows.append({
            "document_id": chunk["document_id"],
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "chunk_number": chunk["chunk_number"],
            "content": chunk["content"],
            "embedding": chunk["embedding"]
        })

    # Remove existing chunks for this document.
    #
    # This makes re-indexing safe.
    document_id = chunks[0]["document_id"]

    (
        supabase
        .table("document_chunks")
        .delete()
        .eq("document_id", document_id)
        .execute()
    )

    # Insert new chunks
    response = (
        supabase
        .table("document_chunks")
        .insert(rows)
        .execute()
    )

    return len(response.data)


# ============================================================
# Update document indexing status
# ============================================================

def mark_indexed(
    document_id,
    chunk_count
):

    indexed_at = datetime.now(
        timezone.utc
    ).isoformat()

    response = (
        supabase
        .table("documents")
        .update({
            "chunk_count": chunk_count,
            "indexed_at": indexed_at
        })
        .eq("id", document_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Failed to update document indexing status."
        )

    return response.data[0]


# ============================================================
# Main indexing function
# ============================================================

def index_document(document_id):

    print(
        f"Indexing document: {document_id}"
    )

    # --------------------------------------------------------
    # 1. Get metadata
    # --------------------------------------------------------

    document = get_document(
        document_id
    )

    status = document.get("status")

    # --------------------------------------------------------
    # 2. Only approved/routed documents can be indexed
    # --------------------------------------------------------

    if status not in [
        "Approved",
        "Routed"
    ]:

        raise ValueError(
            f"Document cannot be indexed "
            f"from status '{status}'. "
            f"Approve and route it first."
        )

    # --------------------------------------------------------
    # 3. Download original document
    # --------------------------------------------------------

    print("Downloading document...")

    file_bytes = download_document(
        document["storage_path"]
    )

    # --------------------------------------------------------
    # 4. Create chunks
    # --------------------------------------------------------

    print("Creating chunks...")

    chunks = build_document_chunks(
        document_id=document["id"],
        filename=document["filename"],
        file_bytes=file_bytes
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    if not chunks:

        raise ValueError(
            "No searchable text could be extracted "
            "from the document."
        )

    # --------------------------------------------------------
    # 5. Generate embeddings
    # --------------------------------------------------------

    print("Generating embeddings...")

    chunks = generate_embeddings(
        chunks
    )

    # --------------------------------------------------------
    # 6. Persist chunks
    # --------------------------------------------------------

    print(
        "Saving chunks to Supabase..."
    )

    saved_count = save_chunks(
        chunks
    )

    # --------------------------------------------------------
    # 7. Update document
    # --------------------------------------------------------

    updated_document = mark_indexed(
        document_id=document_id,
        chunk_count=saved_count
    )

    print(
        f"Indexed {saved_count} chunks"
    )

    return {
        "success": True,
        "document_id": document_id,
        "chunk_count": saved_count,
        "indexed_at": updated_document[
            "indexed_at"
        ]
    }


# ============================================================
# Manual test
# ============================================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python -m src.indexing_service "
            "<document_id>"
        )

        raise SystemExit(1)

    document_id = sys.argv[1]

    result = index_document(
        document_id
    )

    print(
        json.dumps(
            result,
            indent=2,
            default=str
        )
    )