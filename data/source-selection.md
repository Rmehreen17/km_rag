# Source Selection

This document records the exact page ranges and sections selected for the initial RAG corpus.

## Selection Principles

- Prefer substantive business, strategy, AI, financial, policy, compliance, and governance information.
- Preserve original document terminology.
- Preserve original page numbers where available.
- Avoid unnecessary repetitive material.
- Retain enough context for meaningful retrieval.
- Preserve source metadata for citation and evaluation.
- Do not include sections that are only referenced by the source but are not actually present in the uploaded document.

---

# Microsoft Annual Reports

## MSFT-23 — Microsoft 2023 Annual Report

### Selected pages

| Pages | Content |
|---|---|
| 5–6 | AI, responsible AI, trust, privacy, cybersecurity |
| 11–25 | Business, strategy, products and services, operating segments, research and development |
| 27–42 | Management's Discussion and Analysis, financial performance, segment results, market risks |

### Approximate corpus contribution
33 pages

### Notes
The report references "Risk Factors" in the fiscal year 2023 Form 10-K, but a standalone Risk Factors section is not included in this uploaded annual report. Risk Factors are therefore excluded from the initial corpus.

---

## MSFT-24 — Microsoft 2024 Annual Report

### Selected pages

| Pages | Content |
|---|---|
| 5–6 | AI, trustworthy AI, cybersecurity, privacy, digital safety |
| 11–26 | Business, strategy, products and services, operating segments, research and development |
| 27–43 | Management's Discussion and Analysis, financial performance, segment results, market risks |

### Approximate corpus contribution
35 pages

### Notes
The report references "Risk Factors" in the fiscal year 2024 Form 10-K, but a standalone Risk Factors section is not included in this uploaded annual report. Risk Factors are therefore excluded from the initial corpus.

---

## MSFT-25 — Microsoft 2025 Annual Report

### Selected pages

| Pages | Content |
|---|---|
| 4–6 | AI, responsible AI, trust, security, privacy |
| 10–21 | Business, strategy, products and services, operating segments, research and development |
| 22–36 | Management's Discussion and Analysis, financial performance, segment results, market risks |

### Approximate corpus contribution
30 pages

### Notes
The report references "Risk Factors" in the fiscal year 2025 Form 10-K, but a standalone Risk Factors section is not included in this uploaded annual report. Risk Factors are therefore excluded from the initial corpus.

---

# NARA Documents

## NARA-EM-25 — Electronic Messaging Compliance Assessment Toolkit

### Selected pages

| Pages | Content |
|---|---|
| 1–3 | Purpose, records management, security, technical and legal requirements, general best practices |
| 4–6 | Records management best practices and stakeholder responsibilities |
| 7–12 | Assessment questions covering business needs, records management, and agency policy/end-user responsibilities |
| 13–17 | Technical capabilities, security considerations, legal concerns and risk assessments |
| 18 | Conclusion and assessment approach |

### Approximate corpus contribution
18 pages

---

## NARA-EMAIL-16 — Email Management Success Criteria

### Selected pages

| Pages | Content |
|---|---|
| 2–5 | Success criteria: Policies, Systems, Access, Disposition; agency responsibilities |
| 8–10 | Appendix A: Questions to Discuss on Email Management Success Criteria |
| 11–20 | Appendix B: Spreadsheet of Requirements for Email Management |

### Approximate corpus contribution
17 pages

---

## NARA-CAP — The Capstone Approach and Capstone GRS

### Selected pages

| Pages | Content |
|---|---|
| 3–4 | Executive Summary and background |
| 5–8 | Records management guidance and Capstone approach |
| 9–14 | Capstone GRS development, challenges, stakeholder review, internal tests, GRS structure, FAQ, verification and approval |
| 15–18 | Appendix A: Capstone GRS, including Items 010, 011 and 012 |
| 19–27 | Appendix B: FAQs covering implementation, retention, culling, transfer and verification |

### Approximate corpus contribution
25 pages

---

## NARA-ERM — Universal Electronic Records Management Requirements

### Status

Pending upload / source file not currently available in the project attachments.

### Planned selection

- Capture
- Maintenance and Use
- Disposal
- Transfer
- Metadata
- Reporting
- Must Have requirements
- Should Have requirements

The spreadsheet will be handled separately from the PDF/document corpus because its structure is tabular rather than page-based.

---

# Corpus Dimensions

The initial corpus intentionally contains three dimensions:

1. Domain
   - Company Intelligence
   - Records & Information Governance

2. Time
   - Microsoft 2023
   - Microsoft 2024
   - Microsoft 2025
   - NARA documents from different publication periods

3. Document Type
   - Annual reports
   - Compliance toolkit
   - Records-management guidance
   - Email-management criteria
   - White paper / records schedule guidance

---

# Evaluation Goals

The corpus will support experiments involving:

- Chunk size
- Chunk overlap
- Semantic retrieval
- Hybrid retrieval
- Top-k retrieval
- Retrieval precision
- Evidence/citation accuracy
- Cross-domain retrieval
- Cross-year retrieval
- Unanswerable questions
- Failure analysis

---

# Data Provenance

Each document/chunk should retain:

- Document ID
- Source organization
- Document title
- Publication year
- Document type
- Domain
- Source URL
- Original page number where available
- Selected section
