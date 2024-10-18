import chromadb
import argparse
import os
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
#from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma

from app.utils.embedding_function import get_embedding_function

chroma_client = chromadb.HttpClient(host='localhost', port=8000)

DATA_PATH = 'data/pdfs'
CHROMA_PATH = 'data/chroma'

def load_documents():
  # Create a PyPDFDirectoryLoader for loading PDF files
    document_loader_PDF = PyPDFDirectoryLoader(DATA_PATH)
  # Create a JSONLoader for loading JSON files
        # Create a JSONLoader for loading JSON files
    def extract_data(record: dict, metadata: dict) -> tuple[str, dict]:
        # Extraer el contenido principal
        content = f"""
        Nombre: {record.get('name', '')}
        RUC: {record.get('document', '')}
        Dirección: {record.get('address', '')}
        Email: {record.get('email', '')}
        Teléfono: {record.get('phoneNumber', '')}
        Celular: {record.get('mobileNumber', '')}
        Giro del negocio: {record.get('turnOfBusiness', '')}
        """

        # Extraer metadatos relevantes
        metadata['business_id'] = str(record.get('_id', {}).get('$oid', ''))
        metadata['created_at'] = record.get('createdAt', {}).get('$date', '')
        metadata['document_type'] = record.get('documentType', '')
        metadata['country'] = record.get('countryOrigin', '')

        return content, metadata

    # Crear el JSONLoader
    document_loader_JSON = JSONLoader(
        file_path='ruta/a/tu/archivo_business.json',
        jq_schema='.',  # Procesar todo el objeto JSON
        content_key=None,  # No usamos una clave específica, sino una función personalizada
        metadata_func=extract_data
    )

    # Cargar documentos
    documents_PDF = document_loader_PDF.load()
    documents_JSON = document_loader_JSON.load()

    # Combinar documentos
    all_documents = documents_PDF + documents_JSON

    return all_documents


def split_documents(documents: list[Document]) -> list[Document]:
    # Crear un splitter de texto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    # Dividir documentos en pedazos de texto
    documents_split = text_splitter.split_documents(documents)
    return documents_split
  
def add_to_chroma(chunks: list[Document]):
    # Crear un vector store de Chroma
    chroma = Chroma.from_documents(chunks, embedding_function=get_embedding_function())
    # Agregar vectores a la base de datos
    chroma.persist()
    
    # Calculate Page IDs
    chunks_with_ids = calculate_chunk_ids(chunks)
    
    # Add or update chunks in the database
    existing_items = chroma_client.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents: {len(existing_ids)}")
    
    # Only add document that don't exist in the database
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
            print(f"Adding chunk: {chunk.metadata['id']}")
        else:
            print(f"Skipping chunk: {chunk.metadata['id']}")
    
    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        chroma_client.add_documents(new_chunks, ids=new_chunk_ids)
        chroma_client.persist()
    else:
        print("No new documents to add.")


def calculate_chunk_ids(chunks):

    # Esto creará IDs como "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index
    # Página de origen : Número de página : Índice de fragmento

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # Si el ID de página es el mismo que el último, incremente el índice.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calcular el ID de fragmento.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Agregarlo a los metadatos de la página.
        chunk.metadata["id"] = chunk_id

    return chunks
  
def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        
        
def populate_database():
  
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database")
    args = parser.parse_args()
    
    if args.reset:
      print("Resetting database...")
      clear_database()
      
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    
    
if __name__ == "__main__":
    populate_database()