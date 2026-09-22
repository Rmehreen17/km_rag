## 💡 Product Takeaways

Building and evaluating EKS surfaced several product-level insights about enterprise RAG systems.

### 1. Retrieval quality is only one part of the product

A retrieval system can find the correct document without necessarily returning the exact passage needed to answer the user's question.

This means retrieval metrics alone are insufficient for evaluating an enterprise knowledge product.

The evaluation needs to extend from:

**Retrieve → Ground → Cite → Verify → Abstain when necessary**

### 2. Evidence presentation is part of the UX

Users need to understand not only *what* the system answered, but *why* it answered that way.

This led to a deliberate distinction between retrieved candidates and citation-backed supporting evidence.

### 3. Corpus boundaries are a product decision

An AI assistant cannot reliably answer questions about information that does not exist in its knowledge repository.

Rather than hiding this limitation, EKS makes the boundary explicit through abstention.

### 4. Hybrid retrieval involves trade-offs

Semantic retrieval and BM25 solve different retrieval problems.

The experiments showed that combining them can improve the ranking of some answer-bearing passages, but the current evaluation is too small to establish that hybrid retrieval is universally superior.

### 5. Evaluation should influence product design

The retrieval experiments were not treated as a separate technical exercise.

Findings from evaluation directly influenced the product:

- Citation requirements
- Supporting-evidence presentation
- Abstention behavior
- Retrieval strategy
- Corpus boundaries

## 🔮 Future Improvements

The current prototype intentionally focuses on retrieval, grounding, evidence traceability, and abstention.

Potential next iterations include:

- Expand the evaluation set beyond the current 23-question golden set
- Add systematic answer-correctness evaluation
- Add citation-accuracy evaluation
- Evaluate chunk-size and overlap strategies systematically
- Test additional embedding models
- Evaluate reranking approaches
- Improve cross-document and cross-year synthesis
- Add confidence and evidence-quality indicators
- Expand the corpus across additional enterprise domains
