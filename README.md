# ConsciousDay Agent — MVP

Reflect inward. Act with clarity.

## What this delivers
- Streamlit UI for morning inputs (Journal, Dream, Intention, Top 3 Priorities)
- LangChain agent generating **Inner Reflection + Strategy** via OpenRouter (OpenAI-compatible API)
- SQLite (`entries.db`) stores entries
- View past entries by date
- Minimal tests for DB operations

## Files
- `streamlit_app.py` — Streamlit entrypoint  
- `agent/agent.py` — LangChain prompt and runner (OpenRouter-compatible)  
- `db.py` — SQLite helper and schema  
- `tests/test_db.py` — pytest for DB operations  

## Requirements
See `requirements.txt`

---

## Environment Variables
For local development or Streamlit Cloud:

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | Required — your OpenRouter key (OpenAI-compatible). |
| `OPENROUTER_MODEL` | Optional — model to use (default: `gpt-4o-mini`). |
| `OPENAI_API_BASE` | Optional — set to `https://openrouter.ai/api/v1` so OpenRouter works via OpenAI-compatible calls. |

**Note:** The agent automatically sets `OPENAI_API_KEY` and `OPENAI_API_BASE` to enable OpenRouter usage.

---

## Run Locally
1. Install dependencies:

```bash
pip install -r requirements.txt
