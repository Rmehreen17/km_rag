## 🏗️ Architecture

EKS follows an evidence-first RAG pipeline:

```text
Enterprise Documents
        ↓
Document Processing
        ↓
Paragraph-based Chunking
        ↓
MiniLM Embeddings
        ↓
Hybrid Retrieval
   ↙            ↘
Semantic        BM25
   ↘            ↙
     RRF Fusion
          ↓
    Context Builder
          ↓
   Gemini Flash Lite
          ↓
 Grounded Answer
 + Exact Citations
          ↓
  Citation Extraction
       ↙       ↘
Supporting     Insufficient
Evidence       Evidence
    ↓              ↓
Show in UI       Abstain
       ↘         ↙
        Streamlit


| Component            | Implementation                                          |
| -------------------- | ------------------------------------------------------- |
| Document processing  | Page extraction with document and page metadata         |
| Chunking             | Paragraph-based chunking with preserved page boundaries |
| Embeddings           | `sentence-transformers/all-MiniLM-L6-v2`                |
| Semantic retrieval   | Vector similarity                                       |
| Keyword retrieval    | BM25                                                    |
| Retrieval fusion     | Reciprocal Rank Fusion (RRF)                            |
| Context construction | Retrieved document, page, chunk ID, and text            |
| Answer generation    | Gemini Flash Lite                                       |
| Citation format      | Document + page + chunk ID                              |
| Evidence handling    | Supporting evidence extracted from answer citations     |
| Abstention           | Explicit response when evidence is insufficient         |
| UI                   | Streamlit                                               |


![Enterprise Knowledge Search Architecture]](enterprise_knowledge_search_architecture.png)
