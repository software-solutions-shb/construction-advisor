# Local Human-in-the-Loop Advisory System (Phase 1)

This folder defines the **manual** workflow and file structure for a local advisory system. It does **not** implement retrieval or embeddings yet. It prepares the system for Retrieval-Augmented Generation (RAG) by standardizing how expert-approved Q&A is stored.

## What is included
- System prompt for consistent LLM drafting
- Knowledge base format for expert-approved answers
- Manual review workflow and checklist
- JSON schema for future validation

## Quick start (manual)
1) Open the system prompt in prompts/system_prompt.txt and use it when running Ollama.
2) Save LLM drafts into data/drafts/.
3) Human expert reviews and edits the draft.
4) Save the approved response into knowledge_base/approved/ as Markdown with front matter.

## Why this prepares for RAG later
- Each approved entry has structured metadata and clean text.
- A future script can load entries, generate embeddings, and build a vector index.
- Retrieval will then surface the most relevant approved answers for new questions.

## Files and folders
- prompts/system_prompt.txt
- knowledge_base/approved/
- knowledge_base/README.md
- workflows/draft_to_approval.md
- workflows/review_checklist.md
- config/advisory_schema.json
- data/drafts/
