
import os
import logging

from google import genai
from openai import OpenAI

logger = logging.getLogger(__name__)

GEMINI_MODEL_NAME = "gemini-flash-lite-latest"

OPENROUTER_MODEL_NAME = os.environ.get(
    "OPENROUTER_MODEL_NAME",
    "openrouter/free"
)

OPENAI_MODEL_NAME = os.environ.get(
    "OPENAI_MODEL_NAME",
    "gpt-4o-mini"
)


def build_prompt(question, context):
    """
    Build an evidence-first prompt with strict citation requirements.
    """

    return f"""
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


def generate_with_gemini(prompt):
    """
    Generate an answer using Gemini.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt
    )

    answer = response.text

    if not answer:
        raise RuntimeError("Gemini returned an empty response.")

    return answer


def generate_with_openrouter(prompt):
    """
    Generate an answer using OpenRouter.
    Defaults to OpenRouter's free model router.
    """

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not configured.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("OpenRouter returned an empty response.")

    return answer


def generate_with_openai(prompt):
    """
    Generate an answer using OpenAI.
    Retained as the final fallback for future paid API usage.
    """

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("OpenAI returned an empty response.")

    return answer


def generate_grounded_answer(question, context):
    """
    Generate a grounded answer using:
    1. Gemini (primary)
    2. OpenRouter (free fallback)
    3. OpenAI (final fallback)
    """

    prompt = build_prompt(question, context)

    gemini_error_type = "Not attempted"
    openrouter_error_type = "Not attempted"

    # Primary provider: Gemini
    try:
        answer = generate_with_gemini(prompt)

        logger.info("Answer generated successfully using Gemini.")

        return answer

    except Exception as error:
        gemini_error_type = type(error).__name__

        logger.warning(
            "Gemini failed (%s). Trying OpenRouter.",
            gemini_error_type
        )

    # Second provider: OpenRouter
    try:
        answer = generate_with_openrouter(prompt)

        logger.info("Answer generated successfully using OpenRouter.")

        return answer

    except Exception as error:
        openrouter_error_type = type(error).__name__

        logger.warning(
            "OpenRouter failed (%s). Trying OpenAI.",
            openrouter_error_type
        )

    # Final provider: OpenAI
    try:
        answer = generate_with_openai(prompt)

        logger.info("Answer generated successfully using OpenAI.")

        return answer

    except Exception as error:
        openai_error_type = type(error).__name__

        logger.error(
            "All providers failed. Gemini: %s | OpenRouter: %s | OpenAI: %s",
            gemini_error_type,
            openrouter_error_type,
            openai_error_type
        )

        raise RuntimeError(
            "Answer generation failed with all providers. "
            f"Gemini: {gemini_error_type}; "
            f"OpenRouter: {openrouter_error_type}; "
            f"OpenAI: {openai_error_type}"
        ) from error
