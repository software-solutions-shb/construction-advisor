# Backend (Phase 1 MVP)

Local-only FastAPI backend that loads approved knowledge entries from Markdown files and uses a local Ollama LLaMA model to draft responses in Alex’s advisory style.

## Folder expectations
- Approved knowledge lives in: `knowledge/approved/`
- Each file is Markdown with YAML front matter + sectioned content
- Any extra lines at the bottom of the file are treated as **important context**

## Install dependencies
From the repo root:

```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the server
```
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

## Test the /chat endpoint
```
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Do I need an expansion gap for LVP next to tile?"}'
```

## How knowledge is loaded
- The backend scans `knowledge/approved/` for `.md` files.
- YAML front matter is parsed for metadata (question, tags, risk, etc.).
- The body is parsed into sections:
  - Summary of the situation
  - Key considerations
  - Options and trade-offs
  - Suggested next steps
  - Boundaries disclaimer
  - Assumptions
  - Escalation notes
- Any extra lines after the last known section are captured as **Added context notes**.

## How retrieval works (Phase 1)
- Simple keyword overlap + tag matches (no embeddings yet).
- Top 3 entries are passed into the LLaMA prompt.

## How the LLaMA prompt works
- The LLM receives:
  - Your question
  - Relevant approved entries (all sections + added context notes)
  - Alex’s advisory role and boundaries
- It responds in a structured, conservative format.

## Future upgrades (not implemented yet)
- Vector embeddings (sentence-transformers)
- RAG retrieval with FAISS or ChromaDB
- Auth, credits, payments
- Frontend chat integration

## Notes
- Ensure Ollama is running locally with Llama 3.1 8B.
- Configure with environment variables if needed:
  - `OLLAMA_URL` (default: http://localhost:11434/api/generate)
  - `OLLAMA_MODEL` (default: llama3.1:8b)
