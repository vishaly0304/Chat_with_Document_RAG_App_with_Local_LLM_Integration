# 💬 Chat with Document

An interactive Streamlit application that lets you upload and chat with your documents using **Ollama** and **LangChain**. Supports **TXT**, **PDF**, and **DOCX** file formats — all processed locally with zero cloud dependencies.

## 🎥 Live Demo

### Full Video Demo
> **Click to Play:** Opens the full MP4 video.

[![Watch the Full Demo](https://img.shields.io/badge/Watch-Full%20Demo-blue?style=for-the-badge&logo=github)](./assets/demo.mp4)

## ✨ Features

- 📤 **Multi-format Support**: Upload TXT, PDF, and DOCX files
- 🧠 **Local LLM**: Powered by Ollama (Llama 3.2:3b) — no API keys needed
- 🔍 **Semantic Search**: Uses `nomic-embed-text` for high-quality embeddings
- 💾 **Chroma Vector Store**: Efficient document chunking and retrieval
- 💬 **Interactive Chat**: Ask questions and get answers grounded in your document
- 🔒 **Privacy-First**: All processing happens on your machine

## 🛠️ Tech Stack

| Component        | Technology              |
|------------------|-------------------------|
| UI Framework     | Streamlit               |
| LLM              | Ollama (`llama3.2:3b`)  |
| Embeddings       | Ollama (`nomic-embed-text`) |
| Vector Store     | ChromaDB                |
| Document Loading | LangChain Community     |
| Text Splitting   | LangChain Text Splitters|

## 🚀 Project Journey

This project evolved through 3 key iterations:

1.  **v1 (Hardcoded):** Started with a fixed `.txt` file to test the basic RAG pipeline.
2.  **v2 (Dynamic Upload):** Added `st.file_uploader` to allow users to upload any TXT file and manage session state properly.
3.  **v3 (Multi-Format):** Integrated `PyPDFLoader` and `Docx2txtLoader` to support PDF and DOCX files, plus robust error handling and temporary file cleanup.

*Check the **What I Learned** section below for details on the challenges solved in each version!*

## 🧠 What I Learned Building This

- **Session State is Crucial**: Learned to store the `chain` object in `st.session_state` to persist the vector store and model across user interactions, preventing the app from rebuilding the entire database on every click.
- **File Path Requirement**: Discovered that LangChain loaders need a file path, requiring files to be saved to a temporary location before loading and deleted afterwards.
- **Dynamic Loader Logic**: Implemented a robust file extension check (`if/elif/else`) to dynamically select the correct loader class, ensuring the app handles TXT, PDF, and DOCX files without crashing.
- **Warning Suppression**: Added `warnings.filterwarnings()` to suppress `DeprecationWarning` and `PendingDeprecationWarning` for a cleaner console output.
- **Error Handling Flow**: Understood the importance of `st.stop()` to halt execution immediately if file loading or vector store creation fails.
- **Chunking Strategy**: Configured `RecursiveCharacterTextSplitter` with `chunk_size=1000` and `chunk_overlap=200` to balance context preservation with retrieval precision.
- **Retriever Tuning**: Learned to tune the `search_kwargs={"k":5}` parameter to control exactly how many document chunks are retrieved for context, directly impacting answer accuracy vs. processing speed.
- **Local Dependency**: The app fails silently if `nomic-embed-text` or `llama3.2:3b` isn't already installed in Ollama, so I added clear error messages to guide users.

## 🏗️ Architecture

```mermaid
graph LR
  A[📤 Upload<br/>User uploads document<br/>TXT, PDF, DOCX] --> B[📂 Load<br/>App selects loader<br/>by file extension]
  B --> C[✂️ Split<br/>Split into chunks<br/>1000 tokens, 200 overlap]
  C --> D[🧠 Embed<br/>Chunks converted to<br/>vectors nomic-embed-text]
  D --> E[💾 Store<br/>Embeddings stored in<br/>in-memory ChromaDB]
  E --> F[🔍 Retrieve<br/>Top-5 relevant<br/>chunks fetched]
  F --> G[🦙 Generate<br/>Llama 3.2 generates<br/>answer from context]
  G --> H[💬 Display<br/>Answer shown in<br/>chat interface]

  style A fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff
  style B fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
  style C fill:#ec4899,stroke:#db2777,stroke-width:2px,color:#fff
  style D fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
  style E fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
  style F fill:#06b6d4,stroke:#0891b2,stroke-width:2px,color:#fff
  style G fill:#f97316,stroke:#ea580c,stroke-width:2px,color:#fff
  style H fill:#6366f1,stroke:#4f46e5,stroke-width:2px,color:#fff