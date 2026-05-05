# 📄 Smart Document Intelligence System

An AI-powered, full-stack web application designed to revolutionize how we interact with complex PDF documents. By leveraging a **Retrieval-Augmented Generation (RAG)** framework, this system provides precise, context-grounded answers and automatic summarization with near real-time performance.

---

## 🚀 Key Features

- **Intelligent Summarization:** Automatically generates concise, high-level overviews of lengthy documents.
- **Context-Aware Q&A:** Interactive chat interface for retrieving specific information grounded strictly in the uploaded content.
- **Anti-Hallucination Engine:** Grounding responses in retrieved document chunks to ensure factual reliability and accuracy.
- **High-Speed Inference:** Optimized using **Groq's LPU architecture** for low-latency response generation.
- **Scalable Architecture:** Effortlessly handles large documents by splitting text into manageable chunks and using vector-based retrieval.

---

## 🛠️ Tech Stack

### Backend & AI

- **Python:** Core programming language.
- **LangChain:** Orchestrating the RAG pipeline.
- **FastAPI:** High-performance web framework for the backend.
- **Hugging Face:** Utilizing transformer-based models for semantic embeddings.
- **ChromaDB:** Local vector database for efficient document storage and similarity search.

### Frontend

- **Streamlit:** For a clean, user-friendly, and interactive web interface.

---

## 📋 System Requirements

### Software

- Python 3.8+
- Git
- VS Code (Recommended IDE)

### Hardware

- **Processor:** Intel i5 or equivalent (Minimum).
- **RAM:** 8 GB (16 GB Recommended).
- **Storage:** 10–20 GB free space.

---

## ⚙️ How It Works (Methodology)

1.  **Ingestion:** User uploads a PDF document.
2.  **Preprocessing:** Text is extracted, cleaned, and split into smaller, overlapping chunks.
3.  **Embedding:** Chunks are converted into high-dimensional vector embeddings using transformer models.
4.  **Storage:** Vectors are stored in **ChromaDB** for fast semantic retrieval.
5.  **Querying:** User queries are embedded and matched against the document vectors.
6.  **Generation:** The most relevant chunks are passed to a **Large Language Model (LLM)** to generate a grounded, context-aware response.

---

## 👤 Author

**Vikas Sharma**
