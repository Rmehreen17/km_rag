
import os
from google import genai


MODEL_NAME = "gemini-flash-lite-latest"


def create_client():
    """
    Create a Gemini client using the GEMINI_API_KEY
    environment variable.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
        )

    return genai.Client(api_key=api_key)


def generate_grounded_answer(question, context):
    """
    Generate an answer using only the retrieved evidence.
    """

    client = create_client()

    prompt = f"""
You are an evidence-first enterprise knowledge assistant.

Answer the user's question using ONLY the evidence provided below.

Rules:

1. Do not use outside knowledge.
2. Do not invent facts, numbers, dates, or claims.
3. Every factual claim must be supported by the provided evidence.
4. Every factual claim MUST include a citation.
5. Citations MUST use the exact document name, page number, and chunk ID
   provided in the evidence.
6. Use this exact citation format:
   [Document DOCUMENT_NAME, p. PAGE_NUMBER, Chunk ID: CHUNK_ID]

7. Example:
   [Document msft-23, p. 5, Chunk ID: msft-23-P5-C1]

8. Do NOT omit DOCUMENT_NAME from the citation.
9. Do NOT replace DOCUMENT_NAME with the word "Document".
10. Do NOT modify or invent document names, page numbers, or chunk IDs.
11. Copy the citation metadata exactly from the provided evidence.
12. If evidence from multiple documents is needed, clearly distinguish
    the sources.
13. Do not infer an answer simply because related information appears
    in the evidence.
14. If the evidence is insufficient to answer the question, say exactly:
    "I don't have enough evidence in the provided corpus to answer this."
15. Prefer concise answers over unnecessary detail.

USER QUESTION:
{question}

RETRIEVED EVIDENCE:
{context}

Now provide the answer.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
