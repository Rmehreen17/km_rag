# Golden Evaluation Questions

This evaluation set is used to test retrieval quality, answer quality,
citation accuracy, cross-document reasoning, and unanswerable-question behavior.

The questions are intentionally designed to cover different retrieval patterns.

---

## Evaluation Categories

1. Single-document factual retrieval
2. Section-specific retrieval
3. Cross-year retrieval
4. Cross-document comparison
5. Domain-specific terminology
6. Cross-domain retrieval
7. Multi-hop retrieval
8. Evidence/citation testing
9. Unanswerable questions
10. Out-of-corpus questions

---

# A. Company Intelligence

## Q01 — Business strategy

**Question:**  
What are the three interconnected ambitions that Microsoft describes as driving its research and development efforts?

**Expected source:** MSFT-25

**Expected evidence:**  
Business / Research and Development section

**Type:** Single-document factual retrieval

**Answerable:** Yes

---

## Q02 — Operating segments

**Question:**  
What are Microsoft's three reportable operating segments?

**Expected source:** MSFT-25

**Expected evidence:**  
Operating Segments

**Type:** Exact terminology retrieval

**Answerable:** Yes

---

## Q03 — AI and security

**Question:**  
How does Microsoft describe the relationship between AI, security, compliance, and privacy?

**Expected source:** MSFT-25

**Expected evidence:**  
Business / AI / security / responsible AI sections

**Type:** Conceptual retrieval

**Answerable:** Yes

---

## Q04 — 2024 financial performance

**Question:**  
What drove Microsoft's revenue growth in fiscal year 2024 compared with fiscal year 2023?

**Expected source:** MSFT-24

**Expected evidence:**  
Management's Discussion and Analysis

**Type:** Financial retrieval

**Answerable:** Yes

---

## Q05 — 2025 financial performance

**Question:**  
What drove Microsoft's revenue growth in fiscal year 2025 compared with fiscal year 2024?

**Expected source:** MSFT-25

**Expected evidence:**  
Management's Discussion and Analysis

**Type:** Financial retrieval

**Answerable:** Yes

---

## Q06 — Cross-year comparison

**Question:**  
How did Microsoft Cloud revenue change from fiscal year 2024 to fiscal year 2025?

**Expected sources:** MSFT-24, MSFT-25

**Expected evidence:**  
Microsoft Cloud revenue highlights

**Type:** Cross-year retrieval

**Answerable:** Yes

---

## Q07 — AI investment

**Question:**  
What does Microsoft's 2025 annual report say about its research and development investments in cloud and AI?

**Expected source:** MSFT-25

**Expected evidence:**  
Research and Development

**Type:** Terminology-heavy retrieval

**Answerable:** Yes

---

## Q08 — Responsible AI across years

**Question:**  
How did Microsoft's discussion of responsible AI differ between the 2024 and 2025 annual reports?

**Expected sources:** MSFT-24, MSFT-25

**Expected evidence:**  
Responsible AI / trust / governance discussions

**Type:** Cross-year comparison

**Answerable:** Yes

---

# B. Records & Information Governance

## Q09 — Email management success criteria

**Question:**  
What four categories does NARA use to describe success criteria for email management?

**Expected source:** NARA-EMAIL-16

**Expected evidence:**  
Success Criteria section

**Type:** Exact terminology retrieval

**Answerable:** Yes

---

## Q10 — Systems requirements

**Question:**  
What does NARA say an email management system must be able to do before disposition can be executed?

**Expected source:** NARA-EMAIL-16

**Expected evidence:**  
Systems success criterion

**Type:** Requirement retrieval

**Answerable:** Yes

---

## Q11 — Access requirements

**Question:**  
What does NARA mean by ensuring that email records remain usable and retrievable throughout their lifecycle?

**Expected source:** NARA-EMAIL-16

**Expected evidence:**  
Access success criterion

**Type:** Requirement retrieval

**Answerable:** Yes

---

## Q12 — Electronic messaging compliance

**Question:**  
What areas must an electronic messaging application address according to NARA's Electronic Messaging Compliance Assessment Toolkit?

**Expected source:** NARA-EM-25

**Expected evidence:**  
Purpose and assessment areas

**Type:** Multi-factor retrieval

**Answerable:** Yes

---

## Q13 — Stakeholders

**Question:**  
Which stakeholders does NARA identify as having responsibilities in the evaluation and implementation of electronic messaging applications?

**Expected source:** NARA-EM-25

**Expected evidence:**  
Stakeholder List

**Type:** Entity/role retrieval

**Answerable:** Yes

---

## Q14 — Risk assessment

**Question:**  
What does NARA indicate about the risk associated with answering "no" or "unsure" to assessment questions?

**Expected source:** NARA-EM-25

**Expected evidence:**  
Risk Assessment sections

**Type:** Evidence-based reasoning

**Answerable:** Yes

---

# C. Capstone / Records Disposition

## Q15 — Capstone approach

**Question:**  
What is the Capstone Approach intended to simplify or automate in email management?

**Expected source:** NARA-CAP

**Expected evidence:**  
Executive Summary / Capstone Approach

**Type:** Concept retrieval

**Answerable:** Yes

---

## Q16 — Role-based disposition

**Question:**  
How does the Capstone Approach determine disposition of email records?

**Expected source:** NARA-CAP

**Expected evidence:**  
Capstone GRS discussion

**Type:** Conceptual retrieval

**Answerable:** Yes

---

## Q17 — Culling

**Question:**  
What does NARA mean by "culling" in the context of Capstone implementation?

**Expected source:** NARA-CAP

**Expected evidence:**  
Capstone GRS development / culling discussion

**Type:** Domain terminology

**Answerable:** Yes

---

## Q18 — Verification

**Question:**  
Why did the Capstone GRS development team conclude that a verification and approval process was necessary?

**Expected source:** NARA-CAP

**Expected evidence:**  
Verification and Approval Process

**Type:** Reasoning from evidence

**Answerable:** Yes

---

# D. Cross-Domain Questions

## Q19 — Governance comparison

**Question:**  
What similarities can be found between Microsoft's discussion of responsible AI governance and NARA's approach to electronic messaging governance?

**Expected sources:** MSFT-24/MSFT-25 + NARA-EM-25

**Expected evidence:**  
Governance, accountability, requirements, risk, compliance

**Type:** Cross-domain synthesis

**Answerable:** Yes, with evidence from both domains

---

## Q20 — Technology and governance

**Question:**  
How do the Microsoft and NARA documents describe the relationship between technology capabilities and governance requirements?

**Expected sources:** Microsoft reports + NARA-EM-25

**Expected evidence:**  
AI/cloud/security/governance + technical records-management requirements

**Type:** Cross-domain synthesis

**Answerable:** Yes

---

# E. Unanswerable / Abstention Tests

These questions are intentionally outside the available corpus.

The system should **not invent an answer**.

---

## Q21 — Out-of-corpus company information

**Question:**  
What was Microsoft's total revenue in fiscal year 2026?

**Expected source:** None

**Type:** Future/out-of-corpus information

**Answerable:** No

**Expected behavior:**  
State that the available corpus does not contain this information.

---

## Q22 — Missing regulatory source

**Question:**  
What does the UAE Personal Data Protection Law require for retention of personal data?

**Expected source:** None

**Type:** Out-of-corpus regulatory question

**Answerable:** No

**Expected behavior:**  
Do not answer from general knowledge. State that the available corpus does not contain the required source.

---

## Q23 — Missing Microsoft document

**Question:**  
What risks are listed in Microsoft's fiscal year 2025 Form 10-K Risk Factors section?

**Expected source:** None in the current corpus

**Type:** Referenced-but-not-present source

**Answerable:** No

**Expected behavior:**  
Explain that the annual report references the Form 10-K Risk Factors but that section is not included in the current corpus.

---

# Evaluation Dimensions

Each question will eventually be evaluated on:

| Dimension | Description |
|---|---|
| Retrieval Hit | Did the system retrieve relevant evidence? |
| Evidence Relevance | Is the retrieved passage actually useful for answering the question? |
| Answer Correctness | Does the generated answer accurately reflect the evidence? |
| Citation Accuracy | Does the citation point to the supporting evidence? |
| Completeness | Did the answer capture the important parts of the evidence? |
| Abstention | Does the system avoid answering when evidence is unavailable? |
| Cross-Document Retrieval | Can the system retrieve evidence from multiple documents when required? |
| Cross-Year Retrieval | Can the system distinguish information across years? |

---

# Evaluation Philosophy

The goal is not simply to measure whether the LLM can produce a plausible answer.

The evaluation should determine whether the complete RAG system can:

1. Find the right evidence.
2. Use the evidence correctly.
3. Cite the evidence accurately.
4. Distinguish between documents and years.
5. Combine evidence when required.
6. Recognize when the corpus does not contain the answer.
7. Avoid unsupported answers.
