# backend/generation_service.py
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from backend.vector_store import search_similar_chunks

class GenerationService:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.1",
            temperature=0,
            num_ctx=4096
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a precise technical assistant. Your job is to answer the user's question "
                "strictly using the provided text passages. If the answer cannot be confidently derived "
                "from the context, reply exactly with: 'I do not have enough information in the provided documents to answer.'\n\n"
                "Context Passages:\n{context}"
            ),
            ("human", "{question}")
        ])

    async def generate_streaming_answer(self, question: str, top_k: int):
        """Asynchronous generator that yields SSE payloads."""
        # 1. Retrieve Context
        raw_results = search_similar_chunks(question, top_k=top_k)
        
        context_blocks = []
        source_chunks = []
        
        for idx, res in enumerate(raw_results):
            context_blocks.append(f"--- Chunk {idx} ---\n{res['text']}")
            source_chunks.append({
                "chunk_index": res['chunk_index'],
                "text": res['text'],
                "source_document": res['source_document'],
                "relevance_score": res.get('relevance_score', 0.0)
            })
            
        combined_context = "\n\n".join(context_blocks)
        
        # 2. Yield the metadata payload first so the UI can render citations immediately
        metadata_payload = json.dumps({"type": "sources", "data": source_chunks})
        yield f"data: {metadata_payload}\n\n"
        
        # 3. Stream token generation
        if not context_blocks:
            fallback = json.dumps({"type": "token", "content": "I do not have enough information in the provided documents to answer."})
            yield f"data: {fallback}\n\n"
            return
            
        chain = self.prompt_template | self.llm
        
        # astream() asynchronously pulls tokens from Ollama as they are generated
        async for chunk in chain.astream({"context": combined_context, "question": question}):
            token_payload = json.dumps({"type": "token", "content": chunk.content})
            yield f"data: {token_payload}\n\n"