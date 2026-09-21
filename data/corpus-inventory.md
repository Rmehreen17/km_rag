# Corpus Inventory

## Project

Enterprise Knowledge Search

## Objective

Build and evaluate an evidence-first Retrieval-Augmented Generation (RAG)
search experience across a small heterogeneous enterprise knowledge repository.

The initial corpus intentionally contains approximately 200 pages of
high-value material rather than indexing entire source documents.

---

# Domain 1 — Company Intelligence

## MSFT-23 — Microsoft Annual Report 2023

Source: Microsoft Investor Relations

Year: 2023

Document type: Annual Report

Selected content:
- Business and strategy
- AI and responsible AI
- Products and services
- Operating segments
- Management's Discussion and Analysis
- Risk Factors

Target: ~30–35 pages

Purpose:
Provides historical context for Microsoft's business and AI strategy and
allows comparison with later annual reports.

---

## MSFT-24 — Microsoft Annual Report 2024

Source: Microsoft Investor Relations

Year: 2024

Document type: Annual Report

Selected content:
- Business and strategy
- AI and Microsoft Cloud
- Products and services
- Operating segments
- Management's Discussion and Analysis
- Risk Factors

Target: ~30–35 pages

Purpose:
Provides an intermediate point for evaluating how business and AI-related
themes changed over time.

---

## MSFT-25 — Microsoft Annual Report 2025

Source: Microsoft Investor Relations

Year: 2025

Document type: Annual Report

Selected content:
- Business and strategy
- AI and Microsoft Cloud
- Products and services
- Operating segments
- Management's Discussion and Analysis
- Risk Factors
- Selected financial information

Target: ~30–35 pages

Purpose:
Provides the most recent annual-report context in the initial corpus.

---

## Company Intelligence Target

Approximately 90–105 pages.

---

# Domain 2 — Records & Information Governance

## NARA-EM-25 — Electronic Messaging Compliance Assessment Toolkit

Source: U.S. National Archives and Records Administration

Year: 2025

Document type: Compliance assessment toolkit

Selected content:
- Electronic messaging
- Records management
- Stakeholder responsibilities
- Technical considerations
- Security considerations
- Legal/compliance considerations
- Assessment questions

Target: ~15–18 pages

---

## NARA-ERM — Universal Electronic Records Management Requirements

Source: U.S. National Archives and Records Administration

Year: 2023

Document type: Electronic records management requirements

Selected content:
- Capture
- Maintenance and use
- Disposal
- Transfer
- Metadata
- Reporting
- Must Have requirements
- Should Have requirements

Target: ~20–25 pages

Note:
This source is a structured requirements document/spreadsheet and will
be handled separately from the PDF documents.

---

## NARA-EMAIL-16 — Success Criteria for Managing Email Records

Source: U.S. National Archives and Records Administration

Year: 2016

Document type: Guidance / evaluation criteria

Selected content:
- Policies
- Systems
- Access
- Disposition
- Assessment questions
- Requirements

Target: ~15–20 pages

---

## NARA-CAP — Capstone Approach and Capstone GRS

Source: U.S. National Archives and Records Administration

Year: 2014

Document type: White paper / guidance

Selected content:
- Capstone approach
- Rationale
- Role-based disposition
- Retention
- Culling
- Verification
- Capstone GRS items

Target: ~20–25 pages

---

## Records & Information Governance Target

Approximately 75–90 pages.

---

# Overall Corpus Target

Approximately 180–195 pages.

The project does not require an exact page count.

The corpus is intentionally constrained to allow manual evaluation
within a 4–5 day project sprint.

---

# Corpus Dimensions

The corpus provides three useful retrieval dimensions:

## 1. Domain

- Company Intelligence
- Records & Information Governance

## 2. Time

- Microsoft 2023
- Microsoft 2024
- Microsoft 2025
- NARA 2014
- NARA 2016
- NARA 2023
- NARA 2025

## 3. Document Type

- Annual Report
- Guidance
- Compliance Toolkit
- Requirements
- White Paper

---

# Evaluation Goals

The corpus will be used to evaluate:

1. Chunking strategy
2. Semantic retrieval
3. Hybrid retrieval
4. Retrieval precision
5. Citation/evidence accuracy
6. Cross-domain retrieval
7. Cross-year retrieval
8. Unanswerable-question behavior

---

# Data Provenance

Each indexed document will retain:

- Document ID
- Source organization
- Document title
- Publication year
- Document type
- Domain
- Source URL
- Original page number where available
- Selected section

Source documents remain the property of their respective publishers.
The repository will document source information rather than redistribute
documents where redistribution is not appropriate.
