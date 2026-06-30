import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


for k in ("OPENAI_API_KEY", "DATABASE_URL", "COLLECTION_NAME"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(question=None):
    
    # Criar embeddings com OpenAI
    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY
    )

    # Conectar ao vector store PostgreSQL
    vector_connection = PGVector(
        embeddings=embeddings,
        connection=os.getenv("DATABASE_URL"),
        collection_name=os.getenv("COLLECTION_NAME"),
        use_jsonb=True
    )

    # Criar o retriever
    retriever = vector_connection.as_retriever(search_kwargs={"k": 10})
    
    # Criar o prompt
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["contexto", "pergunta"]
    )
  
    # Criar a LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        api_key=OPENAI_API_KEY
    )

    # Função para formatar documentos
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Criar a chain
    chain = (
        {
            "contexto": retriever | format_docs,
            "pergunta": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    if question:
        return chain.invoke(question)

    return chain
