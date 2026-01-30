# Draft → Human Review → Approval Workflow

## Goal
Produce expert-approved answers that can be stored locally and later used for retrieval.

## Manual steps (no retrieval/embeddings yet)
1) Collect the user question and any image references.
2) Run the local LLM (Llama 3.1 via Ollama) with the system prompt.
3) Save the draft response to a file in data/drafts/.
4) Human expert reviews the draft for accuracy, safety, and clarity.
5) Human edits the response as needed and approves it.
6) Save the final response into knowledge_base/approved/ using the template format.
7) Optionally log a short note in the front matter about decisions or constraints.

## Suggested draft filename
- data/drafts/2026-01-29-question-###.md

## Suggested approved filename
- knowledge_base/approved/2026-01-29-topic-###.md

## Minimum acceptance criteria
- Clear boundaries and disclaimers included
- No claims of inspection, certification, or guarantees
- Actionable, realistic next steps
- Risk level tagged appropriately
