from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def chunk_text_file(file_path: str, source_document: str) -> list[dict]:

    text_file_path = Path(file_path)

    if not text_file_path.exists():
        raise FileNotFoundError(
            f"Extracted text file not found: {file_path}"
        )

    text = text_file_path.read_text(
        encoding="utf-8"
    )

    # Remove page markers
    text = re.sub(
        r"--- Page \d+ ---",
        "",
        text
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    text_chunks = text_splitter.split_text(text)

    chunks=[]

    for index, chunk in enumerate(text_chunks):

        cleaned_chunk = chunk.strip()

        # Ignore tiny chunks
        if len(cleaned_chunk) < 100:
            continue

        chunks.append(
            {
                "chunk_index": len(chunks),
                "text": cleaned_chunk,
                "source_document": source_document,
                "character_count": len(cleaned_chunk)
            }
        )

    return chunks