# Create new file: frontend/app.py
import streamlit as st
import requests
import os
import json

# Configuration for connecting to your FastAPI backend
BACKEND_URL = "http://127.0.0.1:8000"

# 1. Page Configuration
st.set_page_config(
    page_title="LocalDoc AI",
    page_icon="📚",
    layout="wide"
)

# 2. Session State Initialization (The Goldfish Notepad)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

st.title("📚 LocalDoc AI: Enterprise RAG")
st.markdown("Upload a technical document and interact with the data in real-time.")

# 3. Sidebar: Document Ingestion Pipeline
with st.sidebar:
    st.header("Document Ingestion")
    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
    
    if uploaded_file is not None and not st.session_state.document_processed:
        with st.spinner("Uploading to Server..."):
            # Prepare the file payload for HTTP POST
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            
            try:
                # Send to our existing FastAPI endpoint
                upload_response = requests.post(f"{BACKEND_URL}/upload", files=files)
                
                if upload_response.status_code == 200:
                    st.success(f"Uploaded: {uploaded_file.name}")
                    
                    # Next Step in Pipeline: Trigger Text Chunking
                    with st.spinner("Extracting and Chunking Text..."):
                        chunk_res = requests.post(f"{BACKEND_URL}/documents/{uploaded_file.name}/chunks")
                        
                        if chunk_res.status_code in [200, 400]: # 400 handles our 'already exists' logic
                            # Final Step: Trigger ChromaDB Indexing
                            with st.spinner("Generating Vector Embeddings..."):
                                index_res = requests.post(f"{BACKEND_URL}/documents/{uploaded_file.name}/index")
                                
                                if index_res.status_code in [200, 400]:
                                    st.success("Document fully indexed and ready for retrieval!")
                                    st.session_state.document_processed = True
                else:
                    st.error("Failed to upload document.")
            
            except requests.exceptions.ConnectionError:
                st.error("Backend server unreachable. Is FastAPI running?")

# Main Chat Area Placeholder (To be built in Commit 2)
st.divider()
# 2. REPLACE the old st.info placeholder with this block:

# Only show the chat interface if a document is ready
if st.session_state.document_processed:
    st.subheader("Chat with your Document")
    
    # Render existing conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Box
    if prompt := st.chat_input("Ask a question about the document..."):
        # 1. Display User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Display Assistant Response
        with st.chat_message("assistant"):
            # Placeholders for dynamic UI updates
            sources_container = st.empty()
            response_placeholder = st.empty()
            full_response = ""
            
            try:
                # Open the persistent SSE connection
                response = requests.post(
                    f"{BACKEND_URL}/ask/stream",
                    json={"question": prompt, "top_k": 3},
                    stream=True  # Crucial for reading SSE
                )
                
                if response.status_code == 200:
                    # Iterate over the incoming stream line by line
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            # Check for the SSE data prefix we set in the backend
                            if decoded_line.startswith("data: "):
                                data_str = decoded_line[6:] # Strip "data: "
                                
                                try:
                                    payload = json.loads(data_str)
                                    
                                    # Handle Metadata (Sources)
                                    if payload["type"] == "sources":
                                        with sources_container.expander("View Retrieved Sources", expanded=False):
                                            for src in payload["data"]:
                                                st.markdown(f"**Score:** {src['relevance_score']:.4f} | **Chunk:** {src['chunk_index']}")
                                                st.caption(f"_{src['text']}_")
                                                st.divider()
                                                
                                    # Handle Text Tokens
                                    elif payload["type"] == "token":
                                        full_response += payload["content"]
                                        # Render with a blinking cursor effect
                                        response_placeholder.markdown(full_response + "▌")
                                        
                                except json.JSONDecodeError:
                                    continue # Skip malformed stream packets
                                    
                    # Remove the cursor when the stream finishes
                    response_placeholder.markdown(full_response)
                else:
                    st.error(f"Backend error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Lost connection to backend server.")
                
            # 3. Save Assistant Message to State
            st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info("👈 Upload and index a document in the sidebar to begin chatting.")