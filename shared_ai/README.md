# Shared AI Foundations

This folder provides reusable building blocks for the 20 portfolio projects:
- OpenAI-compatible LLM client (`LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`)
- Pydantic output schemas
- A tiny explicit tool allowlist
- A place for provider adapters, evaluations and observability

This does **not** mean every app is already integrated with every AI framework. Frameworks overlap and should be selected per use case. Install only the tools a project actually uses. Never commit real `.env` files or secrets.
