# Retrieval Experiment: Post-Retrieval Document Diversity

## Objective

Test whether limiting retrieved results to one chunk per source document improves evidence diversity and retrieval quality.

## Baseline

The baseline hybrid retriever uses Reciprocal Rank Fusion (RRF) across semantic and BM25 retrieval results.

For this experiment, the baseline returns the top 5 hybrid results without post-retrieval filtering.

## Experimental rule

A simple diversity heuristic was tested:

- Maximum 1 retrieved chunk per document
- Preserve the original retrieval order
- Continue through the ranked results until top-k results are selected

## Results

### Query 1: Responsible AI

Baseline:

1. MSFT-23, Page 5
2. NARA-CAP, Page 24
3. MSFT-25, Page 5
4. NARA-CAP, Page 8
5. MSFT-24, Page 12

Filtered:

1. MSFT-23, Page 5
2. NARA-CAP, Page 24
3. MSFT-25, Page 5
4. MSFT-24, Page 12

The filter removed a second NARA-CAP result but did not remove the first irrelevant NARA-CAP result. Therefore, document diversity did not directly improve evidence relevance.

### Query 2: Three Microsoft R&D ambitions

Baseline:

1. MSFT-25, Page 5
2. MSFT-24, Page 11
3. MSFT-25, Page 21
4. MSFT-25, Page 10
5. MSFT-25, Page 21

Filtered:

1. MSFT-25, Page 5
2. MSFT-24, Page 11

The filter removed three additional MSFT-25 results. These results may contain complementary evidence from the same source document, so restricting each document to one chunk reduces evidence coverage.

## Finding

The one-chunk-per-document diversity rule was not adopted into the main retrieval pipeline.

The experiment showed that document diversity and evidence relevance are not equivalent. A source document may legitimately contribute multiple relevant chunks to a query, particularly when answering questions that require multiple pieces of evidence.

## Product implication

Post-retrieval diversification should not be applied as a fixed one-chunk-per-document rule without stronger evidence that it improves retrieval quality.

Future experiments could evaluate more sophisticated approaches such as:

- softer document-level diversity limits
- relevance-aware diversification
- reranking
- query-specific retrieval strategies

For the current MVP, the hybrid retriever remains the baseline retrieval strategy.
