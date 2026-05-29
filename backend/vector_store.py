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

def search_similar_chunks(query: str, top_k: int = 3) -> list[dict]:
    """
    Search ChromaDB for chunks that are semantically similar to the user query.
    """

    # Convert query into an embedding, compare it with stored vectors,
    # and return top_k most similar chunks with scores.
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k,
    )

    formatted_results = []

    for document, score in results:
        formatted_results.append(
            {
                # Original chunk index from saved chunk JSON
                "chunk_index": document.metadata["chunk_index"],

                # Actual retrieved text chunk
                "text": document.page_content,

                # Source PDF/document name
                "source_document": document.metadata["source_document"],

                # Character count stored during chunking
                "character_count": document.metadata["character_count"],

                # Similarity/distance score returned by vector search
                "relevance_score": round(score, 4),
            }
        )

    return formatted_results