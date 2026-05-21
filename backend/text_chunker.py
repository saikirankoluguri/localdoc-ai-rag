from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
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

def save_chunks_to_json(chunks: list[dict], source_document: str) -> str:
    chunks_dir = Path("data/chunks")
    chunks_dir.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(source_document).stem
    chunks_file_path = chunks_dir / f"{safe_filename}_chunks.json"

    chunks_file_path.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return str(chunks_file_path)

def load_chunks_from_json(source_document: str) -> list[dict]:
    chunks_dir = Path("data/chunks")
    safe_filename = Path(source_document).stem
    chunks_file_path = chunks_dir / f"{safe_filename}_chunks.json"

    if not chunks_file_path.exists():
        raise FileNotFoundError(
            f"Chunks file not found for document: {source_document}"
        )

    return json.loads(chunks_file_path.read_text(encoding="utf-8"))