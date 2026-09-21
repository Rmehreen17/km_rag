# Enterprise Knowledge Search — Local Corpus

This folder contains **selected text extracts** from the source documents used for the RAG prototype.

## Why selected extracts?

The MVP intentionally uses a small, representative corpus rather than ingesting every page of every source. The selected sections were documented in `data/source-selection.md`.

## Important

- Keep the original source documents separately.
- The extracted text preserves source-page markers such as `===== SOURCE PAGE 25 =====` so retrieval results can be traced back to the original document page.
- The Microsoft annual reports were uploaded as DOCX files and converted to PDF locally before extraction so page boundaries could be preserved.
- These extracted documents are intended for the local prototype. Do not assume that they should be committed to a public GitHub repository; check the source documents' redistribution terms first.
- The NARA sources are public government documents.
