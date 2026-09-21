
import json
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

from src.context_builder import build_context
from src.answer_generator import generate_grounded_answer


EMBEDDED_FILE = "data/processed/embedded_chunks.json"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class RAGPipeline:

    def __init__(self):

        # Load chunks
        with open(EMBEDDED_FILE, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        # Load embeddings
        self.embeddings = np.array([
            chunk["embedding"]
            for chunk in self.chunks
        ])

        # Load embedding model
        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        # Build BM25 index
        tokenized_chunks = [
            chunk["text"].lower().split()
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def semantic_search(self, query, top_k=5):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        scores = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        indices = scores.argsort()[-top_k:][::-1]

        results = []

        for rank, index in enumerate(indices, start=1):

            chunk = self.chunks[index]

            results.append({
                "rank": rank,
                "document": chunk["document_id"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
                "score": float(scores[index])
            })

        return results

    def bm25_search(self, query, top_k=5):

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(
            query_tokens
        )

        indices = scores.argsort()[-top_k:][::-1]

        results = []

        for rank, index in enumerate(indices, start=1):

            chunk = self.chunks[index]

            results.append({
                "rank": rank,
                "document": chunk["document_id"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
                "score": float(scores[index])
            })

        return results

    def hybrid_search(
        self,
        query,
        top_k=5,
        candidate_k=10,
        rrf_k=60
    ):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        semantic_scores = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        semantic_indices = (
            semantic_scores
            .argsort()[-candidate_k:][::-1]
        )

        query_tokens = query.lower().split()

        bm25_scores = self.bm25.get_scores(
            query_tokens
        )

        bm25_indices = (
            bm25_scores
            .argsort()[-candidate_k:][::-1]
        )

        fused_scores = {}

        for rank, index in enumerate(
            semantic_indices,
            start=1
        ):

            fused_scores[index] = (
                fused_scores.get(index, 0)
                + 1 / (rrf_k + rank)
            )

        for rank, index in enumerate(
            bm25_indices,
            start=1
        ):

            fused_scores[index] = (
                fused_scores.get(index, 0)
                + 1 / (rrf_k + rank)
            )

        hybrid_indices = sorted(
            fused_scores,
            key=fused_scores.get,
            reverse=True
        )[:top_k]

        results = []

        for rank, index in enumerate(
            hybrid_indices,
            start=1
        ):

            chunk = self.chunks[index]

            results.append({
                "rank": rank,
                "document": chunk["document_id"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"],
                "score": float(fused_scores[index])
            })

        return results

    def ask(self, question, top_k=5):

        # Step 1: retrieve
        results = self.hybrid_search(
            question,
            top_k=top_k
        )

        # Step 2: build evidence context
        context = build_context(
            results,
            self.chunks,
            max_chunks=top_k
        )

        # Step 3: generate grounded answer
        answer = generate_grounded_answer(
            question,
            context
        )

        return {
            "question": question,
            "answer": answer,
            "retrieved_evidence": results
        }


if __name__ == "__main__":

    pipeline = RAGPipeline()

    question = "How does Microsoft approach responsible AI?"

    result = pipeline.ask(question)

    print("=" * 70)
    print("QUESTION")
    print("=" * 70)
    print(result["question"])

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(result["answer"])

    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE")
    print("=" * 70)

    for item in result["retrieved_evidence"]:

        print(
            f"Rank {item['rank']} | "
            f"{item['document']} | "
            f"Page {item['page']} | "
            f"{item['chunk_id']}"
        )
