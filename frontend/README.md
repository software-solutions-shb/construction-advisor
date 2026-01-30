# Frontend Chat (Phase 2 UI)

This repository remains a static site. A minimal chat interface on the homepage connects to the local FastAPI backend.

## How to use locally
1) Start the backend:
   ```
   cd backend
   uvicorn main:app --reload
   ```
2) Open the site in your browser:
   - Open index.html directly, or use any local static file server.
3) Scroll to the “Ask Alex (Local demo)” section and submit a question.

## Requirements
- Backend must be running at http://localhost:8000
- Ollama must be running with Llama 3.1 8B

## Test the chat flow
- Enter a question like: “Do I need an expansion gap for LVP next to tile?”
- You should see your message and the AI response appear in the chat window.

## Notes for future upgrades
- The chat is modular and can later support:
  - Authentication / user accounts
  - Credits / payments
  - Persistent chat logs
  - Deployed backend URL

## Files updated for the chat
- index.html (chat section)
- assets/js/main.js (fetch + UI logic)
- assets/css/styles.css (chat styling)
