# Corpus Inventory

## Project

**Enterprise Knowledge Search**

## Purpose

The initial prototype uses a deliberately constrained heterogeneous document corpus to evaluate Retrieval-Augmented Generation (RAG) retrieval, chunking, grounding, and evidence quality.

The initial corpus targets approximately 190–200 pages across two knowledge domains.

---

# Domain 1 — Company Intelligence

## MSFT-01 — Microsoft Annual Report 2025

* **Source:** Microsoft Investor Relations
* **Year:** 2025
* **Document type:** Annual Report
* **Target:** ~40 pages
* **Selection:** Business, AI/product strategy, operating segments, MD&A, risk factors, selected financial/segment information
* **Official source:** Microsoft Investor Relations — 2025 Annual Report

## MSFT-02 — Microsoft Annual Report 2024

* **Source:** Microsoft Investor Relations
* **Year:** 2024
* **Document type:** Annual Report
* **Target:** ~35 pages
* **Selection:** Business, AI/product strategy, operating segments, MD&A, risk factors, selected financial/segment information
* **Official source:** Microsoft Investor Relations — 2024 Annual Report

## MSFT-03 — Microsoft Annual Report 2023

* **Source:** Microsoft Investor Relations
* **Year:** 2023
* **Document type:** Annual Report
* **Target:** ~25 pages
* **Selection:** Business, AI/product strategy, operating segments, MD&A, risk factors
* **Official source:** Microsoft Investor Relations — 2023 Annual Report

### Domain target

Approximately 100 pages.

---

# Domain 2 — Records & Information Governance

## NARA-01 — Electronic Messaging Compliance Assessment Toolkit

* **Source:** U.S. National Archives and Records Administration
* **Year:** 2025
* **Document type:** Compliance assessment toolkit
* **Target:** ~20 pages
* **Topics:** Electronic messaging, stakeholders, risk assessment, compliance, records management
* **Official source:** NARA

## NARA-02 — Universal Electronic Records Management Requirements, Version 3

* **Source:** U.S. National Archives and Records Administration
* **Year:** 2023
* **Document type:** ERM requirements spreadsheet
* **Target:** ~20–25 pages of relevant material
* **Topics:** Capture, maintenance and use, disposal, transfer, metadata, reporting
* **Official source:** NARA

## NARA-03 — Success Criteria for Managing Email Records

* **Source:** U.S. National Archives and Records Administration
* **Year:** 2016
* **Document type:** Guidance / evaluation criteria
* **Target:** ~25 pages
* **Topics:** Policies, systems, access, disposition
* **Official source:** NARA

## NARA-04 — Capstone Approach White Paper

* **Source:** U.S. National Archives and Records Administration
* **Year:** 2014
* **Document type:** White paper
* **Target:** ~20–25 pages
* **Topics:** Capstone approach, email records, appraisal, retention and disposition
* **Official source:** NARA

### Domain target

Approximately 90–95 pages.

---

# Corpus Design Principles

Documents should be:

* Publicly accessible
* From authoritative sources
* Relevant to the selected domain
* Useful for question-answering
* Diverse enough to create retrieval challenges
* Suitable for a portfolio demonstration

The corpus is intentionally constrained to enable rapid experimentation and manual evaluation.

The goal is not to maximize document volume. The goal is to understand and measure retrieval quality.

---

# Retrieval Dimensions

The corpus intentionally provides three retrieval dimensions:

### Domain

Company Intelligence vs. Records & Information Governance

### Time

Microsoft 2023 → 2024 → 2025

### Document Type

Annual Report, Guidance, Requirements, White Paper, Spreadsheet

These dimensions will be used when designing the evaluation dataset.

---

# Data Provenance

Each document will be tracked using:

* Document ID
* Domain
* Source organization
* Document title
* Publication year
* Document type
* Source URL
* Page/section used
* Retrieval metadata

Source documents will not be redistributed in this repository unless their terms permit redistribution. The repository will provide source information and instructions for obtaining the documents where appropriate.
