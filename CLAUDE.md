# CLAUDE.md — claude-md-gen

## Project Overview

CLI + FastAPI web tool that generates production-quality `CLAUDE.md` files for any software
project. Calls the Anthropic Claude API with streaming and writes the result to disk (with a
colored diff if a previous version exists).

## Tech Stack

- Python 3.11+
- **Anthropic Python SDK** — streaming generation via `client.messages.stream()`
- **FastAPI + Uvicorn** — web interface with `StreamingResponse`
- **argparse** — CLI flags and interactive mode
- **python-dotenv** — `.env` support for `ANTHROPIC_API_KEY`
- **ruff** — linting and formatting
- **pytest** — unit tests with `unittest.mock` (no live API calls in tests)

## Key Commands

```bash
# Set up (always use venv)
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"

# CLI — interactive mode (runs when no flags are given)
python -m claude_md_gen.cli

# CLI — flags mode
python -m claude_md_gen.cli \
  --name my-app \
  --type "Web App" \
  --stack "FastAPI, PostgreSQL" \
  --description "Does X" \
  --output CLAUDE.md

# Web server (visit http://localhost:8000)
uvicorn claude_md_gen.api:app --reload

# Lint
ruff check .
ruff format .

# Tests (no ANTHROPIC_API_KEY needed)
pytest tests/ -v
```

## Architecture

```
claude_md_gen/
├── generator.py   — stream_claude_md() + build_user_prompt(); only file touching the Anthropic SDK
├── cli.py         — argparse, interactive prompts, colored diff output
└── api.py         — FastAPI app with GET / (HTML) and POST /generate (StreamingResponse)
static/
└── index.html     — Dark-themed vanilla JS UI; fetch() + ReadableStream for live token display
tests/
├── test_generator.py   — pure unit tests on prompt building (no API)
└── test_api.py         — FastAPI TestClient tests with mocked generator
```

**Key invariant:** `generator.py` is the single source of truth for prompt construction and SDK
usage. The CLI and API are thin wrappers around `stream_claude_md()`.

When adding a new input field, update all four locations:
1. `build_user_prompt()` signature + body in `generator.py`
2. `stream_claude_md()` signature in `generator.py`
3. `GenerateRequest` Pydantic model in `api.py`
4. argparse args + interactive prompts in `cli.py`
5. HTML form in `static/index.html`

## Environment

`ANTHROPIC_API_KEY` must be set — either in `.env` (loaded by python-dotenv) or the shell.
Both the CLI and the API read it via `os.environ.get()` inside `generator.py`.

## Special Claude Instructions

- The web UI is intentionally vanilla JS with zero build tooling — keep it that way.
- Tests mock `stream_claude_md` at the boundary; never add live API calls to the test suite.
- The system prompt in `generator.py::SYSTEM_PROMPT` controls output quality — tune it there,
  not in call sites.
- Always test streaming end-to-end when modifying the API; buffering bugs can silently break UX.
