import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

PDF_PATH = os.getenv("PDF_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

def ingest_pdf():
    """
    Função para ingerir arquivos PDF no banco de dados PostgreSQL - pgVector.
    
    Passos:
    1. Carregar PDF
    2. Dividir em chunks de 1000 caracteres com overlap de 150
    3. Converter em embeddings usando OpenAI Embeddings
    4. Armazenar no PostgreSQL com pgVector
    """
    
    try:
        # Etapa 1: Carregar o PDF
        print(f"Carregando PDF: {PDF_PATH}")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        print(f"PDF carregado com sucesso. Total de páginas: {len(documents)}")
        
        # Etapa 2: Dividir em chunks
        print("Dividindo documento em chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Documento dividido em {len(chunks)} chunks")
        
        # Etapa 3: Criar embeddings
        print("Criando embeddings com OpenAI...")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=OPENAI_API_KEY
        )
        
        # Etapa 4: Armazenar no PostgreSQL com pgVector
        print("Armazenando embeddings no PostgreSQL...")
        vector_store = PGVector.from_documents(
            documents=chunks,
            embedding=embeddings,
            connection=os.getenv("DATABASE_URL"),
            collection_name=os.getenv("COLLECTION_NAME"),
            use_jsonb=True
        )
        print("Ingestão concluída com sucesso!")
        
    except Exception as error:
        print(f"Erro durante a ingestão: {error}")
        raise


if __name__ == "__main__":
    ingest_pdf()