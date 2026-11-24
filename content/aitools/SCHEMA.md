# AI Tools Landscape — taxonomy & record schema (V9, checked Nov 2026)

## Layers and categories (use these exact strings)

### L1 Foundation Models
- `Model APIs & Hubs` — model providers/platforms (OpenAI API, Anthropic API, Google AI Studio/Vertex, Mistral, Cohere, Hugging Face, OpenRouter, Together, Groq, Fireworks…). Individual LLM rankings live on the separate AI Models page; list PLATFORMS here, not each model.

### L2 Builder Stack
- `Agent Frameworks` (LangGraph, CrewAI, AutoGen/MS Agent Framework, OpenAI Agents SDK, Google ADK, PydanticAI, Agno, Strands, Mastra, Semantic Kernel…)
- `LLM App & RAG Frameworks` (LangChain, LlamaIndex, Haystack, DSPy, RAGFlow, GraphRAG, txtai, Flowise, Dify, Langflow…)
- `Vector Databases` (Pinecone, Weaviate, Qdrant, Milvus/Zilliz, Chroma, pgvector, Elasticsearch, Redis, MongoDB Atlas VS, LanceDB, turbopuffer…)
- `Embeddings & Rerankers` (OpenAI/Cohere/Voyage/Jina embeddings, BGE, Nomic, Cohere Rerank…)
- `Data Ingestion & Parsing` (Unstructured, Docling, LlamaParse, Firecrawl, Apify, ScrapeGraphAI, Airbyte, Reducto, Jina Reader…)
- `MCP & Tool Integration` (MCP SDKs, FastMCP, MCP registries, Composio, Smithery, Arcade, Zapier MCP…)
- `Agent Memory` (Mem0, Zep, Letta, LangMem…)
- `Observability & Tracing` (LangSmith, Langfuse, Arize Phoenix, Helicone, W&B Weave, Braintrust tracing, OpenTelemetry GenAI…)
- `Evaluation & Testing` (Ragas, DeepEval, promptfoo, Giskard, Braintrust, TruLens, Evidently…)
- `Guardrails & AI Security` (NeMo Guardrails, Guardrails AI, Lakera, Prompt Security, Protect AI, Azure AI Content Safety, Bedrock Guardrails, Presidio…)
- `Prompt Management` (PromptLayer, Humanloop status?, PromptHub, Agenta, Pezzo…)
- `Inference & Serving` (vLLM, Ollama, llama.cpp, LM Studio, SGLang, TGI, Modal, Baseten, Replicate, LiteLLM gateway, Portkey…)
- `Fine-tuning & Training` (Unsloth, Axolotl, Predibase, OpenPipe, Together fine-tuning…)

### L3 Agents & Automation
- `AI Agents` (general/browser/computer-use agents: ChatGPT agent, Manus, Genspark…)
- `Workflow Automation` (n8n, Zapier, Make, Power Automate, Gumloop, Relay…)
- `Prompt-to-App` (Lovable, Bolt, v0, Replit Agent…)
- `AI IDEs & Code Assistants` (Cursor, Windsurf, GitHub Copilot, JetBrains AI…)
- `Async Coding Agents` (Codex cloud, Devin, Jules, Copilot coding agent…)
- `CLI Coding Agents` (Claude Code, Codex CLI, Gemini CLI, Aider…)
- `Code Review & QA` (CodeRabbit, Graphite, Qodo…)

### L4 Business Functions
`Sales`, `Marketing`, `SEO`, `Customer Support`, `Email & Inbox`, `E-commerce & Retail`, `HR & Recruiting`, `Finance & Accounting`, `Legal`, `Project Management`, `Meetings & Notes`, `Personal Productivity`, `Education & Learning`, `Translation & Language`, `Research & Search`, `Enterprise Search & Knowledge`, `Cybersecurity`, `Data & Analytics`

### L5 Creative & Media
`Writing & Copy`, `Image Generation`, `Design & Brand`, `Video Generation & Editing`, `Avatars & Presenters`, `Voice & Speech`, `Music & Audio`, `Presentations`

## Cost-per-output unit by category (default; override if the category's real billing unit differs)
| Category | unit_of_output |
|---|---|
| Model APIs & Hubs, Embeddings & Rerankers | per 1M tokens (input; note output) |
| Image Generation | per image |
| Video Generation & Editing, Avatars & Presenters | per minute of video |
| Voice & Speech | per minute of audio (TTS) or per hour (STT) — state which |
| Music & Audio | per track |
| Meetings & Notes | per hour transcribed |
| Customer Support | per resolution / per conversation (state which) |
| Email & Inbox (outreach), Sales outreach | per 1,000 emails or per contact credit |
| Workflow Automation | per 1,000 task runs / executions |
| Translation & Language | per 1M characters |
| Data Ingestion & Parsing | per 1,000 pages |
| Vector Databases | per 1M vectors stored / month (or per GB) |
| Observability & Tracing, Evaluation & Testing | per 100k traces / spans |
| Inference & Serving | per GPU-hour or per 1M tokens |
| everything else (seat-based SaaS) | per seat per month |

cost_per_unit_usd = entry paid plan monthly price ÷ units included (or the metered rate). If credits are opaque or pricing is "contact sales", set cost_per_unit_usd = null and cost_basis_note = "Not comparable: <reason>". Never estimate.

## Record schema (one JSON object per tool)
```json
{
  "name": "Tool name as branded",
  "vendor": "Company",
  "layer": "L4 Business Functions",
  "category": "Sales",
  "secondary_categories": [],
  "description": "<=120 chars, own words, what it does",
  "website": "https://official-domain/",
  "pricing_model": "free | freemium | subscription | usage | open-source | open-core | enterprise",
  "free_tier": true,
  "open_source": false,
  "license": null,
  "deployment": ["saas","api","self-hosted","desktop","cli","ide-extension","browser-extension","mobile"],
  "entry_price_usd_month": 20,
  "pro_price_usd_month": 50,
  "price_text": "Free / Pro $20/mo / Business $50/user/mo (annual)",
  "billing_basis": "per user/mo, billed annually",
  "unit_of_output": "per seat per month",
  "units_included_entry": null,
  "cost_per_unit_usd": 20,
  "cost_basis_note": "",
  "french_ui": "yes | no | unknown",
  "canada_data_residency": "yes | no | unknown",
  "use_case_tags": ["Sales & Revenue"],
  "status": "active | acquired | renamed | merged | shutdown | sunsetting",
  "status_note": "",
  "pricing_source_url": "https://…/pricing",
  "source_urls": ["https://…"],
  "checked_date": "2026-11",
  "v8_row": 123,
  "change": "kept | updated | new | removed",
  "confidence": "high | medium | low"
}
```
Rules: prices in USD (convert/mark if only CAD/EUR given: put note in billing_basis). Use official vendor pages as the source of truth for price and status; news/aggregators only for status (acquired/shutdown) and must be cited. `unknown` is fine; guessing is not.

## V9 taxonomy update after red team (supersedes the lists above where different)
- Layer L1 is now `L1 Foundation Models & Assistants`; new category `General AI Assistants` (ChatGPT, Claude, Gemini, Microsoft Copilot, Microsoft 365 Copilot, Grok, Meta AI, Mistral Vibe/Le Chat, Poe, DeepSeek app, Kimi, Qwen Chat, Venice). unit: per seat per month.
- `Prompt Management` + `Evaluation & Testing` merged into `Evaluation & Prompt Management`.
- `Fine-tuning & Training` renamed `Training, Fine-tuning & ML Frameworks` (also holds classic ML frameworks, data labelling, computer-vision platforms).
- `Guardrails & AI Security` renamed `Guardrails, AI Security & Governance` (AI governance tools go here).
- New L2 `Search & Web APIs` (Tavily, Exa, Brave Search API, Parallel, You.com APIs) — unit per 1,000 API calls.
- New L2 `Agent Sandboxes & Browser Infra` (Browserbase, E2B, Daytona, Steel, Hyperbrowser) — unit per browser-hour / per sandbox-hour.
- New L3 `Voice Agents` (Vapi, Retell AI, Synthflow, Bland, PolyAI, AI receptionists like Goodcall/Smith.ai) — unit per minute of call.
- Developer orchestrators (Temporal, Prefect) go in `Workflow Automation` with use_case_tags ["Developer orchestration"].
- New boolean field `canadian_vendor` (true only with evidence of Canadian HQ/founding).
- Observability/eval cost unit is "per 1,000 traces / spans".
- Acquired-but-still-sold products: status "active" + status_note naming the acquirer.
