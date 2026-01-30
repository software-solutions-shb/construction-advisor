# Knowledge Base (Expert-Approved Q&A)

This folder stores expert-approved question-and-answer entries as Markdown files with structured front matter.

## Format
Each entry is a Markdown file with YAML front matter followed by the final approved answer.

### Required front matter fields
- id
- created_at (ISO 8601)
- approved_at (ISO 8601)
- question
- tags (array)
- risk_level (low|medium|high)
- reviewer
- source
- images (array of file names or references)

## Example filename
- approved/2026-01-29-kitchen-layout-001.md

## Why Markdown
- Human-readable for review.
- Easy to parse later for RAG indexing.

## Required answer sections
- Summary of the situation
- Key considerations
- Options and trade-offs
- Suggested next steps
- Boundaries disclaimer
- Assumptions
- Escalation notes

## Future RAG readiness
Later, a simple script can load these entries, extract the `question` and `answer`, generate embeddings, and index them for retrieval.
