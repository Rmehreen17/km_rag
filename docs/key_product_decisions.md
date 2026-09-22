## 🧠 Key Product Decisions

### 1. Evidence before fluency

The system is designed around the principle that a useful enterprise AI answer should be traceable to its underlying evidence.

### 2. Hybrid retrieval rather than a single retrieval strategy

Semantic retrieval helps identify conceptually related passages, while BM25 provides lexical matching for exact terminology.

The two approaches are combined using Reciprocal Rank Fusion.

### 3. Retrieved evidence is not automatically displayed as supporting evidence

The application distinguishes between:

- **Retrieved evidence** — candidate passages returned by retrieval.
- **Supporting evidence** — passages explicitly cited by the generated answer.

Only supporting evidence is presented to the user.

### 4. Abstention is a product behavior

When the corpus does not contain sufficient evidence, the system abstains rather than filling the gap with outside knowledge.

### 5. Evaluation drives product decisions

Retrieval behavior was tested before finalizing the user experience.

The experiments influenced decisions around:

- Hybrid retrieval
- Evidence presentation
- Citation requirements
- Corpus boundaries
- Abstention behavior
