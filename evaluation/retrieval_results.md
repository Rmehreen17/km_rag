
# Retrieval Experiment Results

## 1. Experiment Objective

The retrieval experiment compares three retrieval strategies for the
Enterprise Knowledge Search RAG system:

1. Semantic vector retrieval
2. BM25 lexical retrieval
3. Hybrid retrieval using Reciprocal Rank Fusion (RRF)

The objective is to understand how retrieval behavior changes across
different question types and whether combining semantic and lexical
signals improves the ranking of answer-bearing evidence.

This is an exploratory retrieval evaluation, not an overall RAG
accuracy evaluation.

---

## 2. Evaluation Questions

The experiment uses six representative questions mapped to the stable
golden evaluation set:

| Experiment | Golden ID | Question |
|---|---|---|
| EXP01 | Q03 | How does Microsoft approach responsible AI? |
| EXP02 | Q01 | What are the three interconnected ambitions that drive Microsoft's research and development efforts? |
| EXP03 | Q02 | What are Microsoft's three reportable operating segments? |
| EXP04 | Q09 | What are the four success criteria categories for managing email records? |
| EXP05 | Q06 | How did Microsoft Cloud revenue change from FY2024 to FY2025? |
| EXP06 | Q21 | What was Microsoft's FY2026 revenue? |

EXP01–EXP05 are treated as answerable retrieval questions.

EXP06 is an out-of-corpus question and is evaluated separately for
abstention behavior.

---

## 3. Automated Retrieval Results

The current automated evaluation measures document-level retrieval hit
rate for the five answerable questions.

| Retrieval method | Top-1 document hit rate | Top-5 document hit rate | Answerable questions |
|---|---:|---:|---:|
| Semantic | 100% | 100% | 5 |
| BM25 | 80% | 80% | 5 |
| Hybrid | 100% | 100% | 5 |

These results should not be interpreted as overall RAG accuracy,
answer correctness, or citation accuracy.

A document-level retrieval hit indicates that the expected source
document was retrieved. It does not guarantee that the best passage
was ranked first, that the evidence was sufficient, or that the final
answer was correct.

---

## 4. Question-Level Observations

### EXP01 / Q03 — Responsible AI

**Question:**  
How does Microsoft approach responsible AI?

**Semantic:**  
Rank 1 — `msft-23 P5 C1`

**BM25:**  
The top results were primarily NARA Capstone documents and did not
surface the expected Microsoft evidence in the top five.

**Hybrid:**  
Rank 1 — `msft-23 P5 C1`

**Observation:**  
Semantic retrieval successfully identified the relevant Microsoft
responsible AI discussion. Hybrid preserved the relevant result at
Rank 1.

This query also exposed an evidence-quality issue: retrieval can return
semantically related but irrelevant chunks from another document set.
The final application therefore distinguishes retrieved candidates
from citation-backed supporting evidence.

---

### EXP02 / Q01 — R&D ambitions

**Question:**  
What are the three interconnected ambitions that drive Microsoft's
research and development efforts?

**Semantic:**  
Relevant Microsoft evidence was retrieved, including
`msft-25 P5` and `msft-24 P11`.

**BM25:**  
Rank 1 — `msft-25 P10 C1`

**Hybrid:**  
The answer-bearing Microsoft evidence was retrieved, although hybrid
did not improve the top-ranked result over the strongest individual
retrieval signal for this query.

**Observation:**  
BM25 performed strongly for distinctive terminology closely matching
the source material.

Hybrid retrieval did not consistently improve ranking for this query,
showing that combining retrieval signals does not automatically produce
a better top-ranked passage.

---

### EXP03 / Q02 — Operating segments

**Question:**  
What are Microsoft's three reportable operating segments?

**Semantic:**  
Rank 2 — `msft-25 P22 C2`

**BM25:**  
Rank 4 — `msft-25 P22 C2`

**Hybrid:**  
Rank 1 — `msft-25 P22 C2`

**Observation:**  
Hybrid retrieval improved the ranking of the direct answer-bearing
passage from Rank 2 under semantic retrieval to Rank 1.

All three retrieval methods surfaced the relevant passage within the
top five.

---

### EXP04 / Q09 — Email management success criteria

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

### EXP05 / Q06 — Cross-year Microsoft Cloud comparison

**Question:**  
How did Microsoft Cloud revenue change from FY2024 to FY2025?

**Evidence classification:** Partial evidence.

The retrieved passages contain Microsoft Cloud definitions, revenue
drivers, segment-level cloud revenue information, and overall company
revenue comparisons.

However, the available retrieved evidence does not provide a single
Microsoft Cloud total revenue figure for both FY2024 and FY2025 in the
retrieved passages.

The question therefore requires additional evidence synthesis or a
refinement of the expected answer.

This is classified as partial evidence rather than a simple retrieval
failure.

The final RAG system appropriately avoids inventing a numerical
comparison when the retrieved evidence does not support one.

---

### EXP06 / Q21 — Out-of-corpus question

**Question:**  
What was Microsoft's FY2026 revenue?

**Evidence classification:** Insufficient evidence.

The corpus contains FY2025 and FY2024 financial information, but no
FY2026 revenue figure.

Semantic and hybrid retrieval return related historical evidence rather
than the requested FY2026 information.

This demonstrates why retrieval similarity alone cannot establish
answerability.

The final RAG system abstains rather than inferring FY2026 revenue from
prior-year information.

---

## 5. Retrieval Strategy Findings

### Semantic retrieval

Semantic retrieval performed strongly for conceptual and
meaning-oriented questions and achieved a 100% Top-1 document hit rate
on the five answerable questions evaluated.

### BM25 retrieval

BM25 performed well when distinctive terminology closely matched the
source material.

Its Top-1 document hit rate was 80% on the five answerable questions
in this evaluation.

### Hybrid retrieval

Hybrid retrieval using Reciprocal Rank Fusion achieved a 100% Top-1
document hit rate on the five answerable questions.

It improved ranking for some structured factual queries, such as the
Microsoft operating segments question, but did not consistently
outperform semantic retrieval on this small evaluation set.

The results therefore do not support declaring one retrieval strategy
universally superior.

---

## 6. Evidence Quality Finding

An important finding from the experiment is that **retrieval success
and evidence usefulness are different measures**.

A retriever can return the correct source document while also returning
irrelevant chunks from other documents.

For example, the responsible AI query retrieved relevant Microsoft
evidence alongside NARA Capstone chunks.

The application therefore separates:

**Retrieved candidates**

from

**Supporting evidence**

Supporting evidence is determined from the citations used by the
grounded answer and is what the UI displays to the user.

This prevents irrelevant retrieved candidates from being presented as
evidence for the final answer.

---

## 7. Abstention Finding

The evaluation includes an intentionally out-of-corpus question.

For the FY2026 revenue question, the retriever returns related
historical financial material, but the answer generator does not have
sufficient evidence to support the requested claim.

The application therefore abstains:

> "I don't have enough evidence in the provided corpus to answer this."

The UI also suppresses retrieved chunks and displays:

> "No supporting evidence was found in the provided corpus."

This demonstrates a deliberate failure-handling behavior rather than
treating every retrieved result as sufficient evidence.

---

## 8. Limitations

This is an exploratory evaluation and should be interpreted within the
following limitations:

- The automated retrieval evaluation contains only five answerable
  questions.
- Top-1 and Top-5 metrics are measured at the document level.
- Retrieval hit does not guarantee passage-level evidence relevance.
- The evaluation does not establish statistical significance.
- The experiment does not support a claim that hybrid retrieval is
  universally better than semantic retrieval.
- Cross-document and cross-year questions require evidence synthesis
  beyond a simple single-chunk hit metric.
- Answer correctness, citation accuracy, completeness, and evidence
  relevance require separate evaluation.

---

## 9. Product Takeaway

The experiment suggests that RAG quality should not be evaluated only
by whether a retriever finds a related document.

For an enterprise knowledge product, the more useful chain is:

**Retrieve → Ground → Cite → Verify → Abstain when necessary**

The resulting system is designed to provide answers that are not only
relevant, but also traceable to supporting evidence and explicit about
corpus limitations.
