# Fast-API-AI — RAG System (Retrieval-Augmented Generation)

This repository contains a **Retrieval-Augmented Generation (RAG) API** built with **FastAPI**, designed to enable intelligent, context-aware queries over document collections using **vector-based semantic search**.

The system combines **information retrieval** from a vector database with **large language models** to generate accurate, grounded, and scalable AI responses.

---

## 📌 Project Purpose

This project demonstrates a modern **document-aware AI architecture** capable of:

- Ingesting unstructured data
- Converting documents into vector embeddings
- Performing semantic retrieval based on meaning
- Injecting relevant context into AI-generated responses

It is suitable for **enterprise chatbots**, **internal AI assistants**, **knowledge bases**, **FAQ automation**, and **customer support systems**.

---

## 🛠️ Technology Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Vector Database:** ChromaDB
- **Embedding Model:** Configurable (OpenAI / local / others)
- **ASGI Server:** Uvicorn
- **Default Port:** `8080`

---

## 🧠 RAG Architecture (High-Level)

1. **Document Ingestion**
   - File parsing and preprocessing
   - Text chunking
   - Embedding generation
   - Vector storage in ChromaDB

2. **Semantic Querying**
   - User submits a question
   - Query is converted into embeddings
   - Most relevant document chunks are retrieved via vector similarity

3. **Response Generation**
   - Retrieved context is passed to the LLM
   - The model generates a grounded, context-aware response

---

## 🚀 Core Features

- 📥 **Document Ingestion**
  - Automated document processing
  - Efficient vector indexing
  - Persistent storage with ChromaDB

- 🔍 **Semantic Search**
  - Meaning-based retrieval
  - Not limited to keyword matching

- 🤖 **AI-Powered Answer API**
  - Unified endpoint for questions
  - Dynamic context injection
  - Model-agnostic design

- ⚡ **Scalable Architecture**
  - Stateless API
  - Easy frontend and system integration
  - Cloud and container ready

---

## 💻 Installation & Usage

### 1️⃣ Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate

#Create a virtual environment
python3 -m venv env

#Activate the virtual environment in linux
source env/bin/activate 

#Activate the virtual environment in windows
env\Scripts\activate

#Readme to install fastapi and requirements.txt
pip install -r requirements.txt

#init fastapi
uvicorn app.main:app --reload --port 8080

#run tests
pytest

#run tests with coverage
pytest --cov=app

