# Retrieval Experiment

## Objective

Compare semantic, lexical (BM25), and hybrid retrieval approaches
across representative questions from the golden evaluation set.

The experiment evaluates whether different retrieval strategies
surface relevant evidence at higher ranks and whether retrieval
behavior differs by question type.

## Retrieval Methods

### 1. Semantic Retrieval

Embedding-based retrieval using:

- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Similarity: cosine similarity

### 2. Lexical Retrieval

BM25 keyword retrieval using:

- Library: `rank-bm25`

### 3. Hybrid Retrieval

Reciprocal Rank Fusion (RRF) combining:

- Semantic retrieval
- BM25 retrieval

## Initial Experiment Questions

The initial experiment uses:

- Q01 — Business strategy
- Q02 — Operating segments
- Q03 — AI and security
- Q04 — 2024 financial performance
- Q05 — 2025 financial performance
- Q06 — Cross-year comparison

Additional golden questions will be evaluated in later stages.

## Evaluation Principle

A retrieval method is not considered successful merely because
it returns a semantically related passage.

Retrieved evidence must be sufficiently relevant to support the
answer expected by the golden question.

For unanswerable questions, retrieval of related information
does not constitute a successful answer. The final system must
recognize when the retrieved evidence is insufficient.
