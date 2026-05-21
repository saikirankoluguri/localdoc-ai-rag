from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text_file(file_path: str, source_document: str) -> list[dict]:
    text_file_path = Path(file_path)

    if not text_file_path.exists():
        raise FileNotFoundError(f"Extracted text file not found: {file_path}")

    text = text_file_path.read_text(encoding="utf-8")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  #Each chunk tries to stay around 1000 characters
        chunk_overlap=200,  #Each chunk overlaps 200 characters with the previous chunk
        separators=["\n\n", "\n", ".", " ", ""], #Separators define the points at which the text will be split into chunks
    )

    text_chunks = text_splitter.split_text(text)

    chunks = []

    for index, chunk in enumerate(text_chunks):
        chunks.append(
            {
                "chunk_index": index,
                "text": chunk,
                "source_document": source_document,
                "character_count": len(chunk),
            }
        )

    return chunks