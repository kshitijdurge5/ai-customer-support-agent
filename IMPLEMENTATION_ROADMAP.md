# Roadmap: implementing real GenAI and agentic integrations

## Important
It is not technically sound to force every GenAI framework into all 20 apps. The goal is to demonstrate breadth across the portfolio and a justified, maintainable stack per app. These projects currently have baseline/demo implementations plus integration plans; this roadmap does not claim all integrations are implemented.

## Recommended capability coverage across the portfolio
- LLM APIs: provider-neutral OpenAI-compatible adapter; add provider-specific adapters only when needed.
- Prompting and structured output: versioned prompts and Pydantic models.
- Tool calling: explicit tool registry, input validation, allowlists, timeouts, and approval gates.
- Agent orchestration: LangGraph for stateful workflows; choose CrewAI only for a project where role-based multi-agent coordination adds value.
- RAG: document parsing, chunking, embeddings, vector store, metadata filters, source citations, and retrieval evaluation.
- Data tools: pandas, SQLAlchemy/read-only database access, CSV and JSON exports.
- API: FastAPI + Pydantic for service endpoints where appropriate.
- UI: Streamlit for fast portfolio demos; Flutter only for mobile-focused app.
- Testing: pytest, deterministic fixtures, golden datasets, integration tests with mocked provider responses.
- Observability/evaluation: Python logging; optional LangSmith or equivalent when configured; track latency, token/cost estimates, tool outcomes, and evaluation scores.
- Deployment: Docker and CI workflows after local tests pass; secrets injected through environment variables.
- Power BI: CSV/database exports plus genuine PBIX files built and checked in Power BI Desktop.

## Suggested phases
1. Run all local baseline apps and repair any errors.
2. Add a shared provider adapter, Pydantic output schemas, and safe tool registry.
3. Integrate 4 flagship apps first: support agent, RAG chatbot, workflow agent, and data analyst.
4. Integrate the remaining apps according to their README-specific plan.
5. Add evaluation cases and automated tests; do not rely only on screenshots.
6. Add Docker/CI and deployment documentation.
7. Build and validate 3–4 native Power BI reports using `power_bi/POWER_BI_PBIX_GUIDE.md`.
8. Update every README to distinguish implemented features from planned features and record verified test results.

## Security baseline
Never execute arbitrary model-generated Python or shell. Restrict tools to an allowlist, validate arguments, set timeouts and output limits, require human approval for consequential actions, and never commit API keys or private user data.
