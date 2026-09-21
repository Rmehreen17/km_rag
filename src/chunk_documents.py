
from pathlib import Path
import re
import json


# Folder containing the selected source documents
RAW_DIR = Path("data/raw")

# Folder where processed chunks will be saved
PROCESSED_DIR = Path("data/processed")


def extract_pages(text):
    """
    Split a document using the page markers created during corpus preparation.
    """
    pattern = r"===== SOURCE PAGE (\d+) ====="
    parts = re.split(pattern, text)

    pages = []

    # The first item is content before the first page marker
    for i in range(1, len(parts), 2):
        page_number = int(parts[i])
        page_text = parts[i + 1].strip()

        if page_text:
            pages.append({
                "page": page_number,
                "text": page_text
            })

    return pages


def create_chunks(text, chunk_size=3200, overlap=400):
    """
    Create overlapping text chunks.

    We use characters here rather than tokens to keep the first
    version simple and dependency-free.
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def process_document(file_path):
    """
    Process one document and preserve its page information.
    """

    text = file_path.read_text(encoding="utf-8")

    pages = extract_pages(text)

    document_id = file_path.stem.replace("_selected", "")

    document_chunks = []

    for page in pages:

        chunks = create_chunks(page["text"])

        for chunk_number, chunk_text in enumerate(chunks, start=1):

            document_chunks.append({
                "chunk_id": f"{document_id}-P{page['page']}-C{chunk_number}",
                "document_id": document_id,
                "page": page["page"],
                "text": chunk_text
            })

    return document_chunks


def main():

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    all_chunks = []

    for file_path in sorted(RAW_DIR.glob("*.txt")):

        print(f"Processing: {file_path.name}")

        chunks = process_document(file_path)

        all_chunks.extend(chunks)

        print(f"  Created {len(chunks)} chunks")

    output_file = PROCESSED_DIR / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print()
    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()
