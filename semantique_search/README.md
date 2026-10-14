# Semantic Search (RAG-ready) — Project README

This repository contains a pipeline that converts PDF documents into searchable semantic chunks and stores them in PostgreSQL for semantic retrieval and RAG-style usage.

**Key stages:** PDF → images → OCR → clean → chunk → embeddings → PostgreSQL

**Primary scripts:**
- `main.py`: run the full ingestion pipeline for documents.
- `search_main.py`: run the semantic search / query flow.
- `test_*.py`: small tests that exercise DB, pgvector search and reranking.

**Repository layout (high level):**
- `ocr/` — PDF to images and OCR extraction.
- `preprocessing/` — cleaning and chunking logic.
- `embeddings/` — embedding model wrapper and save helper.
- `database/` — PostgreSQL wrapper (`PostgreSQLDatabase`).
- `retrieval/` — query embedding, pgvector search and reranker.
- `llm/` — local LLM client wrapper (Ollama).

**Note:** This README documents how to set up dependencies and run the project on a local machine (macOS/Linux). Adjust commands for Windows where appropriate.

**Table of Contents**
- **Prerequisites**
- **Install**
- **Database setup**
- **Run ingestion (process PDFs)**
- **Run search**
- **Tests**
- **Troubleshooting**

**Prerequisites**
- **Python:** 3.10 or newer recommended.
- **PostgreSQL:** 14+ and the `pgvector` extension installed (used for vector storage with `VECTOR(384)`).
- **Ollama (optional):** if you want to use the local LLM generator in `llm/generator.py`, run Ollama locally (default client expects http://127.0.0.1:11434).

**System requirements**
- For OCR with `paddleocr`, you may need platform-specific wheel(s) for `paddlepaddle`. See the PaddlePaddle installation guide if `pip install paddleocr` fails on your system.

**Python dependencies**
Install dependencies into a virtual environment. Example packages used in this project:

- `torch` (required by `sentence-transformers` — pick the correct wheel for your platform)
- `sentence-transformers`
- `paddleocr`
- `pymupdf` (imported as `fitz`)
- `psycopg2-binary` (PostgreSQL client)
- `ollama` (Python client for local Ollama server — optional)

You can install these (CPU-friendly example) with:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
# CPU PyTorch (choose the right index for your environment if you need GPU wheels)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers paddleocr pymupdf psycopg2-binary ollama
```

Alternatively create `requirements.txt` and run `pip install -r requirements.txt` (a `requirements.txt` is included in this repo).

**Database setup**
1. Install PostgreSQL and the `pgvector` extension. Example (Homebrew on macOS):

```bash
brew install postgresql
brew install pgvector
# Start Postgres (macOS):
brew services start postgresql
```

2. Create a database and enable the extension (run in `psql` or via a DB client):

```sql
CREATE DATABASE semantic_search;
\c semantic_search
CREATE EXTENSION IF NOT EXISTS vector;
```

3. Run the SQL schema in `database/schema.sql` to create the tables and expected types. From the repo root:

```bash
psql -d semantic_search -f database/schema.sql
```

**Configuration**
- Default DB connection parameters are in `database/postgres_db.py` constructor (`database='semantic_search'`, `user='macbook'`, `host='localhost'`, `port='5432'`).
- You can either modify the constructor call in your runtime or update the file to use environment variables.

**Run the ingestion pipeline (process PDFs)**
1. Place PDFs to index under `data/pdfs/` (or update `main.py` to point at other folders).
2. Run the pipeline:

```bash
source venv/bin/activate
python main.py
```

What `main.py` does:
- Converts each PDF page to an image (`ocr/pdf_to_images.py`).
- Runs OCR on each image (`ocr/paddle_ocr.py`).
- Cleans the OCR text (`preprocessing/clean_text.py`).
- Splits the cleaned text into chunks (`preprocessing/chunk_text.py`).
- Generates embeddings using `embeddings/embedding_model.py` (model: `BAAI/bge-small-en-v1.5`).
- Inserts document metadata, raw OCR text, clean text, chunks, and embeddings into PostgreSQL (`database/postgres_db.py`).

**Run semantic search**
1. Start the environment and ensure the DB has indexed documents.
2. Run the search driver:

```bash
source venv/bin/activate
python search_main.py
```

`search_main.py` uses the retrieval pipeline in `retrieval/`:
- `embed_query.py` encodes a query using the same embedding model.
- `search_pgvector.py` runs a nearest-neighbor search against vectors stored in PostgreSQL.
- `reranker.py` optionally uses a CrossEncoder to re-rank candidate passages.

**Using the local LLM (optional)**
- `llm/generator.py` assumes an Ollama server is available at `http://127.0.0.1:11434` and will call model `mistral:latest`.
- If you want generation (RAG-style answers), ensure Ollama is running and reachable before using `LLMGenerator`.

**Run tests (quick checks)**
Run the small test scripts to validate core pieces:

```bash
source venv/bin/activate
python test_database.py
python test_pgvector.py
python test_rerank.py
```

**Troubleshooting**
- If `paddleocr` fails to import / run, follow the official PaddlePaddle install instructions for macOS/Linux (they provide platform-specific wheels).
- If `sentence-transformers` raises errors about `torch`, install a matching `torch` wheel for your OS (see https://pytorch.org/get-started/locally/).
- Database connection errors: verify Postgres is running, credentials are correct, and `pgvector` extension is created in the `semantic_search` database.

**Files to inspect**
- Ingestion entrypoint: [main.py](main.py)
- Search entrypoint: [search_main.py](search_main.py)
- DB wrapper: [database/postgres_db.py](database/postgres_db.py)
- Schema: [database/schema.sql](database/schema.sql)

If you'd like, I can also:
- Add environment variable support for DB credentials.
- Create a CLI wrapper to process a single PDF.
- Add a Docker Compose file that brings up Postgres with `pgvector` installed.

---
Generated on repository scan. For platform-specific GPU or OS instructions (Torch, PaddlePaddle), follow the official project docs linked above.
