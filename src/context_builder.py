
import json
from pathlib import Path


PROCESSED_FILE = Path("data/processed/embedded_chunks.json")


def load_chunks():
    """Load embedded document chunks."""
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_context(results, chunks, max_chunks=5):
    """
    Build an evidence context from retrieved chunks.

    Each evidence block contains:
    - document
    - page
    - chunk ID
    - source text
    """

    context_blocks = []

    for rank, result in enumerate(
        results[:max_chunks],
        start=1
    ):

        chunk_id = result["chunk_id"]

        # Find the matching chunk
        chunk = next(
            (
                c for c in chunks
                if c["chunk_id"] == chunk_id
            ),
            None
        )

        if chunk is None:
            continue

        block = (
            f"[Evidence {rank}]\n"
            f"Document: {chunk['document_id']}\n"
            f"Page: {chunk['page']}\n"
            f"Chunk ID: {chunk['chunk_id']}\n"
            f"Text:\n{chunk['text']}\n"
        )

        context_blocks.append(block)

    return "\n\n".join(context_blocks)


if __name__ == "__main__":

    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")

    # Example test using the first five chunks
    example_results = [
        {
            "rank": i + 1,
            "chunk_id": chunks[i]["chunk_id"]
        }
        for i in range(min(5, len(chunks)))
    ]

    context = build_context(
        example_results,
        chunks
    )

    print("\n" + "=" * 70)
    print("CONTEXT BUILDER TEST")
    print("=" * 70)
    print(context[:5000])
