# Fast-API-AI — RAG System (Retrieval-Augmented Generation)

Este repositorio contiene una **API de Generación Aumentada por Recuperación (RAG)** desarrollada con **FastAPI**, diseñada para permitir consultas inteligentes sobre documentos mediante **búsqueda semántica basada en embeddings**.

El sistema combina recuperación de información relevante desde una base de datos vectorial con modelos de IA para generar respuestas contextualizadas, precisas y escalables.

---

## 📌 Objetivo del Proyecto

Demostrar una arquitectura moderna de **IA aplicada a documentos**, capaz de:

- Ingerir información no estructurada
- Transformarla en representaciones vectoriales
- Recuperar contexto relevante de forma semántica
- Integrarlo dinámicamente en respuestas generadas por IA

Este enfoque es ideal para **chatbots empresariales**, **asistentes internos**, **bases de conocimiento**, **FAQ inteligentes** y **sistemas de soporte automatizados**.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 100%
- **Framework API:** FastAPI
- **Base de Datos Vectorial:** ChromaDB
- **Modelo de Embeddings:** Configurable (OpenAI / Local / otros)
- **Servidor ASGI:** Uvicorn
- **Puerto por defecto:** `8080`

---

## 🧠 Arquitectura RAG (Alto Nivel)

1. **Ingesta de documentos**
   - Procesamiento de archivos (texto / PDF / etc.)
   - División en chunks
   - Generación de embeddings
   - Almacenamiento en ChromaDB

2. **Consulta semántica**
   - El usuario realiza una pregunta
   - Se generan embeddings de la consulta
   - Se recuperan los fragmentos más relevantes por similitud vectorial

3. **Generación de respuesta**
   - El contexto recuperado se envía al modelo de IA
   - El modelo genera una respuesta informada y contextual

---

## 🚀 Funcionalidades Principales

- 📥 **Ingesta de Documentos**
  - Procesamiento automático
  - Indexación vectorial eficiente
  - Persistencia en ChromaDB

- 🔍 **Búsqueda Semántica**
  - No depende de palabras clave exactas
  - Recuperación basada en significado y contexto

- 🤖 **API de Respuestas con IA**
  - Endpoint unificado para preguntas
  - Integración directa con modelos de lenguaje
  - Respuestas enriquecidas con contexto real

- ⚡ **Arquitectura Escalable**
  - Stateless API
  - Fácil integración con frontend o sistemas externos
  - Lista para contenedores y despliegue cloud

---

## 💻 Instalación y Uso

### 1️⃣ Crear entorno virtual

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

