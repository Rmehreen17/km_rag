# Enterprise Knowledge Search (EKS)

> **An evidence-first RAG application for searching and answering questions across heterogeneous enterprise documents.**

EKS is an experimental Retrieval-Augmented Generation (RAG) application designed to help users find answers across enterprise documents while keeping the underlying evidence visible and traceable.

The system combines:

- Semantic vector retrieval
- BM25 keyword retrieval
- Reciprocal Rank Fusion (RRF)
- Context construction with document and page metadata
- Grounded answer generation using Gemini
- Citation extraction
- Supporting-evidence display
- Explicit abstention when the corpus does not contain sufficient evidence

The project focuses on a product question:

> **How can an enterprise knowledge assistant provide useful answers without losing the evidence needed to verify them?**

---

## 📌 Disclaimer

EKS is an experimental portfolio project using publicly available documents. It is intended for research and demonstration purposes and does not provide professional, legal, financial, or compliance advice.

---

## 🎯 Problem

Enterprise documents often contain valuable information but can be difficult and time-consuming to navigate.

Users may need to search across large document collections to answer questions about:

- Company strategy
- Financial performance
- AI initiatives
- Records management
- Information governance
- Retention and preservation
- Compliance-related processes

Traditional keyword search can miss conceptually related information, while purely semantic retrieval can struggle with exact terminology, names, and domain-specific language.

EKS explores a hybrid retrieval approach while treating **evidence quality and traceability as first-class product requirements**.

---

## 👤 Target Users

### Primary

Business, product, strategy, research, and information-governance professionals who need to extract and verify information from large document collections.

### Secondary

Analysts and researchers who need to quickly locate supporting evidence across multiple documents.

---

## 💡 Product Hypothesis

A combination of semantic and keyword-based retrieval may provide more robust retrieval across heterogeneous enterprise queries than relying on a single retrieval strategy.

The project tests this hypothesis through controlled retrieval experiments and examines not only whether a relevant document is retrieved, but also whether the retrieved evidence is useful for grounding the final answer.

## 📚 Knowledge Repository

The initial corpus contains **6 publicly available source documents**, covering two enterprise knowledge domains.

### Domain 1 — Company Intelligence

Selected Microsoft annual-report content covering:

- Business strategy
- Operating segments
- Financial performance
- Cloud and AI
- Responsible AI
- Business and technology initiatives

Source documents:

- Microsoft Annual Report 2023
- Microsoft Annual Report 2024
- Microsoft Annual Report 2025

### Domain 2 — Records & Information Governance

Selected National Archives and Records Administration (NARA) guidance covering:

- Electronic messaging management
- Records-management requirements
- Compliance assessment
- Disposition
- Governance and preservation

Source documents:

- Electronic Messaging Management Success Criteria
- Electronic Messaging Compliance Assessment Toolkit
- Capstone Records Management White Paper

### Corpus Characteristics

The selected source material is intentionally constrained to make retrieval behavior and evidence quality practical to inspect manually.

The current processed corpus contains:

- **6 source documents**
- **228 chunks**
- **384-dimensional embeddings**
- Page-level metadata
- Document and chunk identifiers

---

## 🔍 Core User Experience

The user can:

1. Ask a natural-language question.
2. Search the enterprise knowledge repository using hybrid retrieval.
3. Receive an answer generated only from retrieved evidence.
4. See citations identifying the source document, page, and chunk.
5. Inspect the supporting evidence cited by the answer.
6. Receive an explicit abstention when the available corpus does not contain sufficient evidence.

### Evidence-First Behavior

EKS deliberately separates:

**Retrieved evidence**

from

**Supporting evidence**

Retrieved chunks are candidate evidence returned by the retrieval system.

Supporting evidence is the subset of retrieved chunks that the generated answer actually cites.

This distinction prevents the interface from presenting every retrieved chunk as if it directly supported the final answer.

### Abstention

The system also includes an explicit out-of-corpus behavior.

When the retrieved evidence is insufficient, the system responds:

> *“I don't have enough evidence in the provided corpus to answer this.”*

The UI then suppresses unsupported evidence rather than encouraging the user to interpret unrelated retrieved content as an answer.
