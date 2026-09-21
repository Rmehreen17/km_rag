
import json
import csv
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROCESSED_FILE = Path("data/processed/embedded_chunks.json")
OUTPUT_CSV = Path("evaluation/retrieval_evaluation.csv")
OUTPUT_METRICS = Path("evaluation/retrieval_metrics.json")


# --------------------------------------------------
# Evaluation questions
# --------------------------------------------------
# These are the six questions from our initial
# retrieval experiment. The IDs below refer to
# experiment IDs, not the permanent golden-question IDs.

QUESTIONS = [
    {
        "id": "EXP01",
        "golden_id": "Q03",
        "question": "How does Microsoft approach responsible AI?",
        "expected_documents": ["msft-23", "msft-24", "msft-25"],
        "evidence_required": True
    },
    {
        "id": "EXP02",
        "golden_id": "Q01",
        "question": "What are the three interconnected ambitions driving Microsoft's R&D?",
        "expected_documents": ["msft-25"],
        "evidence_required": True
    },
    {
        "id": "EXP03",
        "golden_id": "Q02",
        "question": "What are Microsoft's three reportable operating segments?",
        "expected_documents": ["msft-25", "msft-24", "msft-23"],
        "evidence_required": True
    },
    {
        "id": "EXP04",
        "golden_id": "Q09",
        "question": "What are the success criteria for electronic mail management?",
        "expected_documents": ["nara-email-16"],
        "evidence_required": True
    },
    {
        "id": "EXP05",
        "golden_id": "Q06",
        "question": "How did Microsoft Cloud revenue change from FY2024 to FY2025?",
        "expected_documents": ["msft-24", "msft-25"],
        "evidence_required": True
    },
    {
        "id": "EXP06",
        "golden_id": "Q21",
        "question": "What was Microsoft's FY2026 revenue?",
        "expected_documents": [],
        "evidence_required": False
    }
]


# --------------------------------------------------
# Load corpus
# --------------------------------------------------

print("Loading embedded chunks...")

with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks.")


# --------------------------------------------------
# Prepare embeddings
# --------------------------------------------------

embeddings = np.array([
    chunk["embedding"]
    for chunk in chunks
])

print(f"Embedding matrix: {embeddings.shape}")


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# --------------------------------------------------
# BM25 index
# --------------------------------------------------

tokenized_chunks = [
    chunk["text"].lower().split()
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_chunks)


# --------------------------------------------------
# Semantic search
# --------------------------------------------------

def semantic_search(query, top_k=5):

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    scores = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    indices = scores.argsort()[-top_k:][::-1]

    results = []

    for rank, index in enumerate(indices, start=1):

        chunk = chunks[index]

        results.append({
            "rank": rank,
            "document": chunk["document_id"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "score": float(scores[index])
        })

    return results


# --------------------------------------------------
# BM25 search
# --------------------------------------------------

def bm25_search(query, top_k=5):

    query_tokens = query.lower().split()

    scores = bm25.get_scores(query_tokens)

    indices = scores.argsort()[-top_k:][::-1]

    results = []

    for rank, index in enumerate(indices, start=1):

        chunk = chunks[index]

        results.append({
            "rank": rank,
            "document": chunk["document_id"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "score": float(scores[index])
        })

    return results


# --------------------------------------------------
# Hybrid Reciprocal Rank Fusion
# --------------------------------------------------

def hybrid_search(
    query,
    top_k=5,
    candidate_k=10,
    rrf_k=60
):

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    semantic_scores = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    semantic_indices = (
        semantic_scores
        .argsort()[-candidate_k:][::-1]
    )

    query_tokens = query.lower().split()

    bm25_scores = bm25.get_scores(query_tokens)

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

        chunk = chunks[index]

        results.append({
            "rank": rank,
            "document": chunk["document_id"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "score": float(fused_scores[index])
        })

    return results


# --------------------------------------------------
# Retrieval evaluation
# --------------------------------------------------

def evaluate_results(results, expected_documents):

    retrieved_documents = [
        result["document"]
        for result in results
    ]

    if not expected_documents:

        # Out-of-corpus / abstention question
        return {
            "top1_hit": False,
            "top5_hit": False,
            "contains_expected_document": False
        }

    top1_hit = (
        results[0]["document"]
        in expected_documents
    )

    top5_hit = any(
        document in expected_documents
        for document in retrieved_documents
    )

    return {
        "top1_hit": top1_hit,
        "top5_hit": top5_hit,
        "contains_expected_document": top5_hit
    }


# --------------------------------------------------
# Run evaluation
# --------------------------------------------------

all_rows = []

methods = {
    "semantic": semantic_search,
    "bm25": bm25_search,
    "hybrid": hybrid_search
}


for question in QUESTIONS:

    print()
    print("=" * 70)
    print(
        f"{question['id']} "
        f"(Golden {question['golden_id']}): "
        f"{question['question']}"
    )
    print("=" * 70)

    for method_name, search_function in methods.items():

        results = search_function(
            question["question"],
            top_k=5
        )

        evaluation = evaluate_results(
            results,
            question["expected_documents"]
        )

        for result in results:

            row = {
                "experiment_id": question["id"],
                "golden_question_id": question["golden_id"],
                "question": question["question"],
                "method": method_name,
                "rank": result["rank"],
                "document": result["document"],
                "page": result["page"],
                "chunk_id": result["chunk_id"],
                "score": result["score"],
                "top1_hit": evaluation["top1_hit"],
                "top5_hit": evaluation["top5_hit"],
                "expected_documents": "|".join(
                    question["expected_documents"]
                ),
                "evidence_required": question["evidence_required"]
            }

            all_rows.append(row)

        print(
            f"{method_name:10s} | "
            f"Top-1: {evaluation['top1_hit']} | "
            f"Top-5: {evaluation['top5_hit']} | "
            f"Rank-1 document: {results[0]['document']}"
        )


# --------------------------------------------------
# Save detailed results
# --------------------------------------------------

OUTPUT_CSV.parent.mkdir(
    parents=True,
    exist_ok=True
)

fieldnames = [
    "experiment_id",
    "golden_question_id",
    "question",
    "method",
    "rank",
    "document",
    "page",
    "chunk_id",
    "score",
    "top1_hit",
    "top5_hit",
    "expected_documents",
    "evidence_required"
]

with open(
    OUTPUT_CSV,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(all_rows)


# --------------------------------------------------
# Calculate metrics
# --------------------------------------------------

metrics = {}

for method_name in methods:

    method_rows = [
        row
        for row in all_rows
        if row["method"] == method_name
    ]

    question_results = {}

    for question in QUESTIONS:

        rows = [
            row
            for row in method_rows
            if row["experiment_id"] == question["id"]
        ]

        question_results[question["id"]] = {
            "top1_hit": bool(rows[0]["top1_hit"]),
            "top5_hit": bool(rows[0]["top5_hit"])
        }

    # Only evaluate retrieval hit rate on questions
    # where evidence is expected to exist.
    answerable_questions = [
        q for q in QUESTIONS
        if q["evidence_required"]
    ]

    top1_hits = sum(
        question_results[q["id"]]["top1_hit"]
        for q in answerable_questions
    )

    top5_hits = sum(
        question_results[q["id"]]["top5_hit"]
        for q in answerable_questions
    )

    metrics[method_name] = {
        "answerable_questions": len(answerable_questions),
        "top1_hit_rate": (
            top1_hits / len(answerable_questions)
        ),
        "top5_hit_rate": (
            top5_hits / len(answerable_questions)
        ),
        "out_of_corpus_question": "EXP06",
        "out_of_corpus_behavior": (
            "retrieval evaluated separately; "
            "final answer should abstain"
        )
    }


# --------------------------------------------------
# Save metrics
# --------------------------------------------------

with open(
    OUTPUT_METRICS,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metrics,
        f,
        indent=2
    )


print()
print("=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)

print(f"Results saved to: {OUTPUT_CSV}")
print(f"Metrics saved to: {OUTPUT_METRICS}")

print()
print("Retrieval metrics:")
print(json.dumps(metrics, indent=2))
