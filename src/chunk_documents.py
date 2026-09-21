from pathlib import Path
import re
import json


# ---------------------------------------------------------
# Folders
# ---------------------------------------------------------

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


# ---------------------------------------------------------
# Chunking configuration
# ---------------------------------------------------------

# Approximate character equivalents for our first baseline.
# We will evaluate these values later.
TARGET_CHUNK_SIZE = 3200
OVERLAP_SIZE = 400


# ---------------------------------------------------------
# Page extraction
# ---------------------------------------------------------

def extract_pages(text):
    """
    Split a document using the page markers created
    during corpus preparation.
    """

    pattern = r"===== SOURCE PAGE (\d+) ====="

    parts = re.split(pattern, text)

    pages = []

    for i in range(1, len(parts), 2):

        page_number = int(parts[i])
        page_text = parts[i + 1].strip()

        if page_text:
            pages.append({
                "page": page_number,
                "text": page_text
            })

    return pages


# ---------------------------------------------------------
# Paragraph splitting
# ---------------------------------------------------------

def split_into_paragraphs(text):
    """
    Split text into paragraphs while removing
    unnecessary whitespace.
    """

    paragraphs = re.split(r"\n\s*\n", text)

    cleaned = []

    for paragraph in paragraphs:

        paragraph = re.sub(r"\s+", " ", paragraph).strip()

        if paragraph:
            cleaned.append(paragraph)

    return cleaned


# ---------------------------------------------------------
# Natural chunking
# ---------------------------------------------------------

def create_chunks(text):
    """
    Create chunks using paragraph boundaries.

    Paragraphs are combined until the target chunk size
    is reached. We avoid cutting paragraphs wherever possible.
    """

    paragraphs = split_into_paragraphs(text)

    chunks = []

    current_paragraphs = []
    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(paragraph)

        # If adding the paragraph keeps us within the target
        if current_length + paragraph_length <= TARGET_CHUNK_SIZE:

            current_paragraphs.append(paragraph)
            current_length += paragraph_length

        else:

            # Save the current chunk
            if current_paragraphs:

                chunk_text = "\n\n".join(current_paragraphs)
                chunks.append(chunk_text)

            # Start a new chunk
            current_paragraphs = [paragraph]
            current_length = paragraph_length

    # Save the final chunk
    if current_paragraphs:

        chunk_text = "\n\n".join(current_paragraphs)
        chunks.append(chunk_text)

    return chunks


# ---------------------------------------------------------
# Process one document
# ---------------------------------------------------------

def process_document(file_path):

    text = file_path.read_text(encoding="utf-8")

    pages = extract_pages(text)

    document_id = file_path.stem.replace("_selected", "")

    document_chunks = []

    for page in pages:

        chunks = create_chunks(page["text"])

        for chunk_number, chunk_text in enumerate(chunks, start=1):

            document_chunks.append({

                "chunk_id":
                    f"{document_id}-P{page['page']}-C{chunk_number}",

                "document_id":
                    document_id,

                "page":
                    page["page"],

                "text":
                    chunk_text
            })

    return document_chunks


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------

def main():

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    all_chunks = []

    for file_path in sorted(
        RAW_DIR.glob("*.txt")
    ):

        print(
            f"Processing: {file_path.name}"
        )

        chunks = process_document(
            file_path
        )

        all_chunks.extend(chunks)

        print(
            f"  Created {len(chunks)} chunks"
        )

    output_file = (
        PROCESSED_DIR /
        "chunks.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()

    print(
        f"Total chunks created: "
        f"{len(all_chunks)}"
    )

    print(
        f"Saved to: {output_file}"
    )


# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
