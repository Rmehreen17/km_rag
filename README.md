# Enterprise Knowledge Search (EKS)

#### 📌Disclaimer

EKS is an experimental portfolio project using publicly available documents. It is intended for research and demonstration purposes and does not provide professional, legal, financial, or compliance advice.

### Evidence-First RAG Search Across Enterprise Documents

EKS is an experimental Retrieval-Augmented Generation (RAG) application designed to help users find reliable, evidence-backed answers across heterogeneous enterprise documents.

The initial prototype combines two knowledge domains:

- Company Intelligence — selected technology company annual reports
- Records & Information Governance — public records-management guidance

The goal is not simply to generate answers, but to evaluate how retrieval strategy, chunking, and document structure affect the quality and reliability of evidence returned to users.

## 🎯 Problem

Enterprise documents often contain valuable information but can be difficult and time-consuming to navigate.

Users may need to search across hundreds of pages to answer questions about:

- Company strategy
- Financial performance
- Business risks
- AI initiatives
- Records management
- Information governance
- Retention and preservation

Traditional keyword search can miss conceptually related information, while purely semantic search can struggle with exact terminology and identifiers.

EKS explores whether a combination of retrieval approaches can provide more reliable evidence-backed answers.

## 👤 Target Users

### Primary

Business, product, strategy, research, and information-governance professionals who need to extract information from large document collections.

### Secondary

Analysts and researchers who need to quickly locate and verify information across multiple documents.

## 💡 Product Hypothesis

A RAG system combining semantic and keyword-based retrieval may retrieve relevant evidence more reliably than semantic retrieval alone, particularly for queries containing domain-specific terminology, names, and exact concepts.

This hypothesis will be tested through controlled retrieval experiments.

## 📚 Initial Knowledge Repository

The prototype will contain approximately 200 pages of publicly available documents.

### Domain 1 — Company Intelligence

Approximately 100 pages of selected technology company annual reports.

### Domain 2 — Records & Information Governance

Approximately 100 pages of publicly available records-management and information-governance guidance.

The corpus will be intentionally constrained to enable rapid experimentation and manual evaluation.

## 🔍 Core User Experience

The user should be able to:

1. Ask a natural-language question
2. Retrieve relevant passages from the knowledge repository
3. Receive an answer grounded in those passages
4. View the source document and supporting evidence
5. Understand when sufficient evidence is not available

## 🧪 Experiments

The project will evaluate:

### Chunking

- Small chunks
- Medium chunks
- Larger chunks
- Section-aware chunking where applicable

### Retrieval

- Semantic/vector retrieval
- Hybrid retrieval

### Retrieval parameters

- Top-k
- Retrieval threshold

### Evaluation

- Retrieval hit rate
- Answer correctness
- Citation accuracy
- Abstention / "answer not found" behavior
- Cross-domain retrieval precision

## ❓ Evaluation Questions

The evaluation set will contain questions covering:

- Factual retrieval
- Semantic retrieval
- Exact terminology
- Financial information
- Strategy
- Risk
- Cross-document questions
- Cross-domain questions
- Unanswerable questions

## 🏗️ High-Level Architecture

```text
Public Documents
       ↓
Document Processing
       ↓
Chunking
       ↓
Knowledge Index
       ↓
Retrieval
       ↓
LLM
       ↓
Answer + Evidence
       ↓
User Interface
