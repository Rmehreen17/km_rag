def build_context(
    results,
    max_chunks=5
):
    """
    Build an evidence context directly from
    Supabase retrieval results.
    """

    context_blocks = []

    for rank, result in enumerate(
        results[:max_chunks],
        start=1
    ):

        block = (
            f"[Evidence {rank}]\n"
            f"Document: {result['document']}\n"
            f"Page: {result['page']}\n"
            f"Chunk ID: {result['chunk_id']}\n"
            f"Text:\n{result['text']}\n"
        )

        context_blocks.append(
            block
        )

    return "\n\n".join(
        context_blocks
    )