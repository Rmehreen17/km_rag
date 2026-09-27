import json
import os

from google import genai


MODEL_NAME = "gemini-flash-lite-latest"

#This handles the AI metadata extraction.

def create_client():

    api_key = os.environ.get(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable "
            "is not set."
        )

    return genai.Client(
        api_key=api_key
    )


def extract_metadata(
    filename,
    document_text
):

    client = create_client()

    # Limit metadata prompt size so very large
    # documents do not create unnecessarily large requests.
    text_for_metadata = document_text[:30000]

    prompt = f"""
You are an enterprise document metadata assistant.

Analyze the document below and return metadata as JSON.

DOCUMENT FILENAME:
{filename}

DOCUMENT CONTENT:
{text_for_metadata}

Return ONLY valid JSON using exactly this structure:

{{
    "title": "",
    "department": "",
    "sensitivity": "",
    "tags": [],
    "summary": ""
}}

Rules:

1. title should describe the document.
2. department should identify the most appropriate business
   department when reasonably evident.
3. sensitivity should be one of:
   "Public",
   "Internal",
   "Confidential",
   "Restricted"

4. tags should contain 3-7 useful topic tags.
5. summary should be concise.
6. Do not invent information that is not supported by the document.
7. If something cannot be determined, use "General" where
   appropriate rather than inventing a specific department.
8. Return JSON only.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    raw_text = response.text.strip()

    # Handle occasional markdown fences.
    if raw_text.startswith("```"):
        raw_text = raw_text.replace(
            "```json",
            "",
            1
        )

        raw_text = raw_text.replace(
            "```",
            "",
            1
        ).strip()

    metadata = json.loads(
        raw_text
    )

    return metadata
