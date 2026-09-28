import re

from sentence_transformers import SentenceTransformer

from src.supabase_client import supabase
from src.context_builder import build_context
from src.answer_generator import generate_grounded_answer


# ============================================================
# CONFIGURATION
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DEFAULT_TOP_K = 5
DEFAULT_CANDIDATE_K = 10
DEFAULT_RRF_K = 60


class RAGPipeline:

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        print("Loading RAG embedding model...")

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        print("RAG pipeline ready.")

    # ========================================================
    # SEMANTIC SEARCH
    # ========================================================

    def semantic_search(
        self,
        query,
        candidate_k=DEFAULT_CANDIDATE_K
    ):
        """
        Semantic retrieval using Supabase pgvector.

        The query is converted into an embedding and sent
        to the match_document_chunks PostgreSQL RPC.
        """

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        response = supabase.rpc(
            "match_document_chunks",
            {
                "query_embedding": query_embedding,
                "match_count": candidate_k
            }
        ).execute()

        results = []

        for item in response.data:

            results.append({
                "document_id": item["document_id"],
                "chunk_id": item["chunk_id"],
                "page": item["page"],
                "chunk_number": item["chunk_number"],
                "content": item["content"],
                "similarity": float(
                    item["similarity"]
                )
            })

        return results

    # ========================================================
    # KEYWORD SEARCH
    # ========================================================

    def keyword_search(
        self,
        query,
        candidate_k=DEFAULT_CANDIDATE_K
    ):
        """
        Keyword retrieval using PostgreSQL full-text search.

        IMPORTANT:
        This uses the search_document_chunks RPC created
        in Supabase.

        It does NOT use Supabase .text_search(), because
        that previously caused tsquery parsing errors.
        """

        response = supabase.rpc(
            "search_document_chunks",
            {
                "search_query": query,
                "match_count": candidate_k
            }
        ).execute()

        results = []

        for item in response.data:

            results.append({
                "document_id": item["document_id"],
                "chunk_id": item["chunk_id"],
                "page": item["page"],
                "chunk_number": item["chunk_number"],
                "content": item["content"]
            })

        return results

    # ========================================================
    # RECIPROCAL RANK FUSION
    # ========================================================

    def reciprocal_rank_fusion(
        self,
        semantic_results,
        keyword_results,
        top_k=DEFAULT_TOP_K,
        rrf_k=DEFAULT_RRF_K
    ):
        """
        Combines semantic and keyword retrieval using
        Reciprocal Rank Fusion (RRF).

        RRF score:

            1 / (k + rank)
        """

        fused_scores = {}

        result_lookup = {}

        # ----------------------------------------------------
        # Add semantic results
        # ----------------------------------------------------

        for rank, result in enumerate(
            semantic_results,
            start=1
        ):

            key = (
                result["document_id"],
                result["chunk_id"]
            )

            fused_scores[key] = (
                fused_scores.get(key, 0.0)
                + 1.0 / (rrf_k + rank)
            )

            result_lookup[key] = result

        # ----------------------------------------------------
        # Add keyword results
        # ----------------------------------------------------

        for rank, result in enumerate(
            keyword_results,
            start=1
        ):

            key = (
                result["document_id"],
                result["chunk_id"]
            )

            fused_scores[key] = (
                fused_scores.get(key, 0.0)
                + 1.0 / (rrf_k + rank)
            )

            # If this chunk only came from keyword search,
            # preserve that result.
            if key not in result_lookup:

                result_lookup[key] = result

        # ----------------------------------------------------
        # Rank fused results
        # ----------------------------------------------------

        ranked_keys = sorted(
            fused_scores.keys(),
            key=lambda key: fused_scores[key],
            reverse=True
        )

        ranked_keys = ranked_keys[:top_k]

        results = []

        for rank, key in enumerate(
            ranked_keys,
            start=1
        ):

            result = result_lookup[key]

            results.append({
                "rank": rank,
                "document": result["document_id"],
                "page": result["page"],
                "chunk_id": result["chunk_id"],
                "chunk_number": result["chunk_number"],
                "score": float(
                    fused_scores[key]
                ),
                "text": result["content"]
            })

        return results

    # ========================================================
    # HYBRID SEARCH
    # ========================================================

    def hybrid_search(
        self,
        query,
        top_k=DEFAULT_TOP_K,
        candidate_k=DEFAULT_CANDIDATE_K,
        rrf_k=DEFAULT_RRF_K
    ):
        """
        Hybrid retrieval:

            Semantic search
                    +
            Keyword search
                    ↓
                  RRF
                    ↓
                 Top K
        """

        semantic_results = self.semantic_search(
            query,
            candidate_k=candidate_k
        )

        keyword_results = self.keyword_search(
            query,
            candidate_k=candidate_k
        )

        return self.reciprocal_rank_fusion(
            semantic_results=semantic_results,
            keyword_results=keyword_results,
            top_k=top_k,
            rrf_k=rrf_k
        )

    # ========================================================
    # SUPPORTING EVIDENCE
    # ========================================================

    def extract_supporting_evidence(
        self,
        answer,
        retrieved_results
    ):
        """
        Attempts to match citations generated by the LLM
        against the retrieved chunks.
        """

        citation_pattern = re.compile(
            r"\[(?:Document\s+)?"
            r"([^,\]]+),\s*"
            r"p\.\s*(\d+),\s*"
            r"(?:Chunk ID:\s*)?"
            r"([^\]]+)\]"
        )

        cited_sources = citation_pattern.findall(
            answer
        )

        cited_keys = set()

        for document, page, chunk_id in cited_sources:

            try:
                page_value = int(page)
            except ValueError:
                page_value = page

            cited_keys.add(
                (
                    document.strip(),
                    page_value,
                    chunk_id.strip()
                )
            )

        supporting_evidence = []

        for result in retrieved_results:

            result_key = (
                result["document"],
                result["page"],
                result["chunk_id"]
            )

            if result_key in cited_keys:

                supporting_evidence.append(
                    result
                )

        return supporting_evidence

    # ========================================================
    # ASK
    # ========================================================

    def ask(
        self,
        question,
        top_k=DEFAULT_TOP_K
    ):
        """
        Complete RAG pipeline:

            Question
                ↓
            Hybrid retrieval
                ↓
            RRF
                ↓
            Context builder
                ↓
            Gemini
                ↓
            Grounded answer
        """

        # ----------------------------------------------------
        # Retrieve evidence
        # ----------------------------------------------------

        results = self.hybrid_search(
            query=question,
            top_k=top_k
        )

        # ----------------------------------------------------
        # Build context
        # ----------------------------------------------------

        context = build_context(
            results,
            max_chunks=top_k
        )

        # ----------------------------------------------------
        # Generate answer
        # ----------------------------------------------------

        answer = generate_grounded_answer(
            question,
            context
        )

        # ----------------------------------------------------
        # Detect abstention
        # ----------------------------------------------------

        abstained = (
            "I don't have enough evidence in the provided corpus"
            in answer
        )

        # ----------------------------------------------------
        # Supporting evidence
        # ----------------------------------------------------

        supporting_evidence = []

        if not abstained:

            supporting_evidence = (
                self.extract_supporting_evidence(
                    answer,
                    results
                )
            )

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {
            "question": question,
            "answer": answer,
            "retrieved_evidence": results,
            "supporting_evidence": supporting_evidence,
            "abstained": abstained
        }


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    pipeline = RAGPipeline()

    question = (
        "How does the electronic messaging "
        "compliance toolkit help federal agencies?"
    )

    result = pipeline.ask(
        question
    )

    print("\n")
    print("=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(
        result["answer"]
    )

    print("\n")
    print("=" * 70)
    print("RETRIEVED EVIDENCE")
    print("=" * 70)

    for item in result["retrieved_evidence"]:

        print("\n")
        print(f"Rank: {item['rank']}")
        print(f"Document: {item['document']}")
        print(f"Page: {item['page']}")
        print(f"Chunk: {item['chunk_id']}")
        print(f"RRF Score: {item['score']}")

        print(
            f"Text: {item['text'][:700]}"
        )

    print("\n")
    print("=" * 70)
    print("STATUS")
    print("=" * 70)

    print(
        f"Abstained: {result['abstained']}"
    )

    print(
        f"Retrieved chunks: "
        f"{len(result['retrieved_evidence'])}"
    )

    print(
        f"Supporting evidence: "
        f"{len(result['supporting_evidence'])}"
    )