## 🧪 Evaluation & Results

The retrieval layer was evaluated using a small, manually defined set of questions covering factual, semantic, terminology-heavy, cross-year, and out-of-corpus queries.

The evaluation compares three retrieval strategies:

- Semantic vector retrieval
- BM25 keyword retrieval
- Hybrid retrieval using Reciprocal Rank Fusion (RRF)

### Retrieval Results

| Retrieval Strategy | Top-1 Document Hit | Top-5 Document Hit |
|---|---:|---:|
| Semantic | 100% | 100% |
| BM25 | 80% | 80% |
| Hybrid RRF | 100% | 100% |

**Evaluation scope:** 5 answerable experiment questions.

These are **document-level retrieval hit rates**, not overall RAG accuracy. They do not measure answer correctness, citation accuracy, completeness, or evidence quality.

### What the Experiments Showed

#### 1. Semantic retrieval performed strongly on the evaluated questions

Semantic retrieval successfully identified the relevant source document for all five answerable questions in the evaluation set.

It was particularly useful for conceptually phrased questions such as responsible AI and strategy-related queries.

#### 2. BM25 added value for distinctive terminology

BM25 performed less consistently overall, but it was useful for queries containing distinctive terminology and exact concepts.

For example, the R&D ambitions query surfaced an answer-bearing Microsoft passage at the top of the BM25 results.

#### 3. Hybrid retrieval improved some passage-level rankings

Hybrid retrieval did not universally outperform semantic retrieval.

However, for the operating-segments question, the direct answer-bearing passage moved from rank 2 with semantic retrieval to rank 1 with hybrid retrieval.

This suggests that combining semantic similarity with lexical matching can improve ranking for some enterprise queries, while still requiring further evaluation before making a broader performance claim.

#### 4. Retrieval success is not the same as evidence quality

Some queries returned a relevant document but also included unrelated chunks from other documents.

This led to an important product distinction:

> **Retrieval candidates are not automatically supporting evidence.**

EKS therefore extracts the citations actually used by the generated answer and displays only those chunks as **Supporting Evidence**.

#### 5. The system recognizes corpus gaps

An explicit out-of-corpus question was included in the evaluation.

For example, a question asking for Microsoft FY2026 revenue cannot be answered from a corpus containing the selected FY2023–FY2025 material.

Instead of inferring or hallucinating a value, EKS abstains:

> *“I don't have enough evidence in the provided corpus to answer this.”*

This makes corpus boundaries visible to the user rather than hiding them behind a generated answer.

---

## 🔬 Evaluation Dimensions

The broader evaluation framework considers:

- Retrieval hit
- Evidence relevance
- Answer correctness
- Citation accuracy
- Completeness
- Abstention behavior
- Cross-document retrieval
- Cross-year retrieval

The current automated retrieval experiment is intentionally narrower than the full evaluation framework.

Additional answer-level and evidence-level evaluation remains future work.

---

## ⚠️ Evaluation Limitations

The current results should be interpreted within their experimental scope:

- Only 5 answerable questions were used for the automated retrieval comparison.
- Results are measured at the document level.
- The evaluation set is manually constructed and relatively small.
- No statistical significance testing was performed.
- Retrieval hit does not guarantee that the retrieved passage fully answers the question.
- Answer correctness and citation accuracy require separate evaluation.
- Cross-document and cross-year synthesis require additional testing.

The results therefore demonstrate the behavior of this prototype rather than establishing a universally superior retrieval strategy.
