# Desafio MBA Engenharia de Software com IA - Full Cycle

Projeto simples de busca semântica em PDF usando LangChain, OpenAI, PostgreSQL e pgvector.

## Requisitos

- Python 3.10 ou superior
- Docker e Docker Compose
- Chave de API da OpenAI

## Configuração

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis:

```env
OPENAI_API_KEY=
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
COLLECTION_NAME=semantic-search
PDF_PATH=document.pdf
```

## Instalação

Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Banco de dados

Suba o PostgreSQL com pgvector:

```bash
docker compose up -d
```

Verifique se o container está rodando:

```bash
docker compose ps
```

## Ingestão do PDF

Execute a ingestão do documento:

```bash
python src/ingest.py
```

Esse comando lê o arquivo definido em `PDF_PATH`, divide o conteúdo em chunks, gera embeddings e salva no PostgreSQL com pgvector.

## Chat

Depois da ingestão, execute o chat:

```bash
python src/chat.py
```

Digite uma pergunta no terminal. Para sair, use o atalho `Ctrl + C` um dos comandos:

```text
sair
exit
quit
```