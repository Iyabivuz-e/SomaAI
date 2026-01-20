
NOTE: THE FOLLOWING IS JUST FOR THE FOLDER STRUCTURE, AND SOME CLASSES/METHODS WITH DOT STRINGS TO MAKE THE UNDERSTANDING WHAT ONE DOES. PLEASE, DO NOT DO THE IMPLEMENTATION OF ANY CLASS OR ANY METHOD.

PLEASE AND PLEASE, PAY ATTENTION TO WHAT IS NOTED IN THE NOTE(WRITTEN IN THE CAPITAL LETTERS).

You are a senior backend engineer. Read my repo structure (FastAPI in src/somaai) and produce a step-by-step task list to update the backend to match the product requirements below. Keep it monolithic and minimal; do not overengineer. The output must be a numbered checklist with clear acceptance criteria for each step.

PRODUCT REQUIREMENTS (UPDATED)
Student mode:
- grade + subject selection
- ask question -> RAG answer
- if insufficient -> fallback response
- answer includes citations: doc + page numbers + stable open link
- “show sources” uses citations endpoint
- optional: analogy + real-world context follow-ups or included when enabled

Teacher mode:
- teacher chat like student
- teacher must choose classes taught (multiple)
- teacher defaults: analogy + real-world context enabled by default; teacher can disable
- every teacher response supports feedback: “was this useful?” (boolean + optional text/tags)
- quiz generator:
  - uses topics in DB
  - inputs: topic_ids, difficulty, num_questions
  - option: include detailed answer keys with curriculum citations
  - store quiz result
  - download: questions only OR questions+answers (pdf first OK)

REQUIRED ENDPOINTS
Add:
- GET /api/v1/meta/grades
- GET /api/v1/meta/subjects?grade=
- GET /api/v1/meta/topics?grade=&subject=
- POST/GET /api/v1/teacher/profile
- POST /api/v1/quiz/generate
- GET /api/v1/quiz/{quiz_id}
- GET /api/v1/quiz/{quiz_id}/download?variant=questions|questions_answers&format=pdf|docx (pdf OK first)

Update:
- POST /api/v1/chat/ask (student+teacher)
- GET /api/v1/chat/messages/{message_id}
- GET /api/v1/chat/messages/{message_id}/citations
- POST /api/v1/feedback (requires message_id)
- POST /api/v1/ingest (return job_id)
- GET /api/v1/ingest/jobs/{job_id}
- GET /api/v1/docs/{doc_id}
- GET /api/v1/docs/{doc_id}/view?page=

Keep:
- POST /api/v1/retrieval/search (debug)

CRITICAL ARCH DECISIONS
- Add contracts layer: src/somaai/contracts/*.py for all Pydantic schemas (chat/docs/quiz/teacher/feedback/common/errors)
- Introduce minimal background jobs for ingest + quiz (Redis-backed). Avoid long tasks in request thread.
- Persist citations reliably (documents/chunks/messages/message_citations)

DB MODELS (minimal)
- documents, chunks, messages, message_citations, teacher_profiles, feedback, topics, quizzes, quiz_items
- migrations via Alembic

STORAGE
- Support local file storage now.
- Optionally support Google Drive storage behind env flag STORAGE_BACKEND=local|gdrive with a minimal adapter, no UI auth.

TESTS
- Minimal pytest for meta endpoints, chat response shape, feedback requires message_id, quiz generate shape.

DOCS
- Update docs/api.md and docs/architecture.md

Your task list should include:
- which files to create/edit
- acceptance criteria (e.g., “/chat/ask returns message_id, sufficiency, citations”)
- ordering that minimizes refactors
Return only the checklist.
