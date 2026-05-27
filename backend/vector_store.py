from pathlib import Path
import json

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


# Create embedding model instance
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Create ChromaDB instance
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="data/chroma_db"
)


def load_chunks(source_document: str) -> list[dict]:
    """
    Reads saved chunk JSON file
    """

    safe_filename = Path(source_document).stem

    chunks_file = (
        Path("data/chunks")
        / f"{safe_filename}_chunks.json"
    )

    if not chunks_file.exists():
        raise FileNotFoundError(
            f"Chunks not found: {source_document}"
        )

    return json.loads(
        chunks_file.read_text(
            encoding="utf-8"
        )
    )


def index_document_chunks(
    source_document: str
) -> int:
    """
    Generate embeddings and store in ChromaDB
    """

    chunks = load_chunks(
        source_document
    )

    texts = []
    metadatas = []
    ids = []

    for chunk in chunks:

        texts.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "source_document":
                chunk["source_document"],

                "chunk_index":
                chunk["chunk_index"],

                "character_count":
                chunk["character_count"]
            }
        )

        ids.append(
            f"{source_document}_{chunk['chunk_index']}"
        )

    vector_store.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids
    )

    return len(chunks)

def document_already_indexed(
    source_document: str
) -> bool:
    """
    Check whether document already exists in vector DB
    """

    results = vector_store.get()

    metadata_list = results.get(
        "metadatas",
        []
    )

    for metadata in metadata_list:

        if (
            metadata["source_document"]
            == source_document
        ):
            return True

    return False