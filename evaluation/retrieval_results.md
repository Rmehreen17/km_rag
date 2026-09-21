# Retrieval Experiment Results

## Baseline Retrieval Comparison

The initial experiment compares three retrieval strategies:

1. Semantic vector retrieval
2. BM25 lexical retrieval
3. Hybrid retrieval using Reciprocal Rank Fusion (RRF)

The experiment uses six representative questions from the golden
evaluation set.

---

## Results Summary

| Question | Semantic | BM25 | Hybrid | Initial Observation |
|---|---:|---:|---:|---|
| Q01 — Business strategy | 1 | — | 1 | Semantic and hybrid retrieve relevant evidence at Rank 1 |
| Q02 — Operating segments | 2 | 1 | 4* | BM25 surfaces exact terminology most effectively |
| Q03 — AI and security | — | — | — | Requires evidence-level review |
| Q04 — 2024 financial performance | 1 | 1 | 1 | All methods retrieve the same relevant evidence |
| Q05 — 2025 financial performance | — | — | — | Requires evidence-level review |
| Q06 — Cross-year comparison | — | — | — | Requires multi-document evidence review |

> `—` means the initial experiment output has not yet been classified
> for evidence relevance.

> `*` Q02 requires evidence-level review because another retrieved
> Microsoft chunk may also contain valid evidence.

---

## Detailed Observations

### Q01 — Business strategy

**Question:**  
How does Microsoft approach responsible AI?

**Semantic:**  
Rank 1 — `msft-23 P5 C1`

**BM25:**  
Top results were primarily NARA Capstone documents and did not surface
the expected Microsoft evidence in the top five.

**Hybrid:**  
Rank 1 — `msft-23 P5 C1`

**Observation:**  
Semantic retrieval successfully identified the relevant Microsoft
responsible AI discussion. Hybrid preserved the relevant result at
Rank 1.

---

### Q02 — Operating segments / R&D ambitions

**Question:**  
What are the three interconnected ambitions that drive Microsoft's
research and development efforts?

**Semantic:**  
Rank 2 — `msft-24 P11 C1`

**BM25:**  
Rank 1 — `msft-25 P10 C1`

**Hybrid:**  
Rank 4 — `msft-25 P10 C1`

**Observation:**  
BM25 performed strongly for the terminology-heavy query because the
query contains distinctive phrases appearing in the source material.

Semantic retrieval identified relevant evidence but ranked another
semantically related passage first.

Hybrid did not improve the top-ranked result for this query.

---

### Q03 — Operating segments

**Question:**  
What are Microsoft's three reportable operating segments?

**Semantic:**  
Rank 2 — `msft-25 P22 C2`

**BM25:**  
Rank 4 — `msft-25 P22 C2`

**Hybrid:**  
Rank 1 — `msft-25 P22 C2`

**Observation:**  
Hybrid retrieval improved the ranking of the answer-bearing passage
from Rank 2 under semantic retrieval to Rank 1.

**Evidence classification:** Direct evidence.

All three retrieval methods surfaced the answer-bearing passage
within the top five. Hybrid retrieval ranked the direct evidence
first, improving its position from Rank 2 under semantic retrieval
to Rank 1.

---

### Q04 — Email management success criteria

**Question:**  
What are the four success criteria categories for managing email
records?

**Semantic:**  
Rank 1 — `nara-email-16 P11 C1`

**BM25:**  
Rank 1 — `nara-email-16 P11 C1`

**Hybrid:**  
Rank 1 — `nara-email-16 P11 C1`

**Observation:**  
All three retrieval methods successfully identified the same
answer-bearing passage at Rank 1.

---
### Q05 - 

**Evidence classification:** Partial evidence.

The retrieved passages contain Microsoft Cloud definitions, revenue
drivers, segment-level cloud revenue information, and overall company
revenue comparisons. However, the available retrieved evidence does
not provide a single Microsoft Cloud total revenue figure for both
FY2024 and FY2025.

This means the question requires either evidence synthesis from
additional chunks or refinement of the expected answer.

The result is therefore classified as partial retrieval rather than
a retrieval failure.

-----------

### Q06 -

**Evidence classification:** Insufficient evidence.

The corpus contains FY2025 and FY2024 financial information, but no
FY2026 revenue figure. Semantic and hybrid retrieval return related
FY2025 evidence rather than the requested FY2026 information.

This demonstrates why retrieval similarity alone cannot establish
answerability. The final RAG system should abstain rather than infer
FY2026 revenue from prior-year information.

--------

## Initial Findings

The experiment provides early evidence that retrieval behavior varies
by question type.

### Semantic retrieval

Semantic retrieval performed well for conceptual and meaning-oriented
questions, including the responsible AI query.

### BM25 retrieval

BM25 performed particularly well when the query contained distinctive
terminology or phrases closely matching the source material.

### Hybrid retrieval

Hybrid retrieval improved ranking for some structured factual queries,
such as the Microsoft operating segments question, but did not
consistently outperform semantic or BM25 retrieval.

### Important finding

The experiment does not support declaring one retrieval method as
universally superior.

The results suggest that retrieval strategy should be evaluated
against the type of question being asked.

---

## Limitations of the Initial Experiment

This is an exploratory retrieval experiment rather than the final
evaluation of the RAG system.

The initial results use six representative questions and require
additional evidence-level classification before final retrieval
metrics are calculated.

Some questions require:

- multiple chunks
- multiple documents
- cross-year comparison
- evidence synthesis

Therefore, a simple "exact chunk retrieved = success" metric is
insufficient for the complete golden evaluation set.

The final evaluation will separately measure:

- Retrieval Hit
- Evidence Relevance
- Cross-Document Retrieval
- Cross-Year Retrieval
- Abstention
- Answer Correctness
- Citation Accuracy
- Completeness
