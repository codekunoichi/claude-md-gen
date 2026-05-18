# ⚡ CLAUDE.md Generator

> Describe your project → get a production-ready `CLAUDE.md` for Claude Code sessions.

A CLI + FastAPI web tool that calls the Anthropic Claude API (with streaming) to generate a `CLAUDE.md` for any software project. Drop the output in your repo root and Claude Code has instant context every session.

---

## Features

- **Interactive CLI** — run with no flags and answer prompts, or pass everything via flags for scripted use
- **Streaming output** — tokens print live to the terminal (or browser) as they arrive
- **Diff on update** — colored unified diff when a `CLAUDE.md` already exists
- **Web UI** — dark-themed single-page form, no build step required
- **Installable package** — exposes a `claude-md-gen` entry point after `pip install`

## Quick start

```bash
# 1. Clone & set up
git clone https://github.com/codekunoichi/claude-md-gen.git
cd claude-md-gen
python3 -m venv venv && source venv/bin/activate
pip install -e .

# 2. Set your API key
export ANTHROPIC_API_KEY=sk-ant-...
# or add it to a .env file

# 3. Generate
claude-md-gen
```

## CLI usage

### Interactive mode

Run with no flags — you'll be prompted for each field:

```bash
claude-md-gen
```

```
⚡ CLAUDE.md Generator

  Project name: ink-to-calendar
  Project type (Web App, CLI, Library, API, …): Web App
  What does it do?: Photographs handwritten planner and schedules tasks
  Tech stack: Python, FastAPI, Qwen2-VL, SQLite
  Key commands (leave blank to skip): python main.py --env mac
  Architecture notes (leave blank to skip): Two-env config with symlink pattern
  Special Claude instructions (leave blank to skip):

Generating with claude-sonnet-4-6…
────────────────────────────────────────────────────────────
# ink-to-calendar
...
```

### Flag mode

```bash
claude-md-gen \
  --name "my-api" \
  --type "API" \
  --description "REST API for task management" \
  --stack "FastAPI, PostgreSQL, Redis" \
  --commands "uvicorn main:app --reload\npytest" \
  --arch "Repository pattern, async SQLAlchemy" \
  --instructions "Always check migration state before schema changes" \
  --output CLAUDE.md
```

### All flags

| Flag | Description |
|------|-------------|
| `--name` | Project name |
| `--type` | Project type (Web App, CLI, Library, API, …) |
| `--description` | What the project does |
| `--stack` | Tech stack |
| `--commands` | Key shell commands |
| `--arch` | Architecture notes |
| `--instructions` | Special Claude instructions |
| `--output` | Output path (default: `CLAUDE.md`) |
| `--model` | Claude model (default: `claude-sonnet-4-6`) |
| `--no-interactive` | Disable prompts; fail if required fields missing |

## Web UI

```bash
uvicorn claude_md_gen.api:app --reload
# open http://localhost:8000
```

Fill in the form, click the arrow — tokens stream into the output panel. Copy to clipboard or download `CLAUDE.md` directly.

## Project structure

```
claude_md_gen/
├── generator.py   — Anthropic SDK streaming; single source of truth for prompt logic
├── cli.py         — argparse CLI, interactive prompts, colored diff
└── api.py         — FastAPI app (GET / → HTML, POST /generate → StreamingResponse)
static/
└── index.html     — Vanilla JS web UI; no build tooling
tests/
├── test_generator.py
└── test_api.py
```

## Development

```bash
pip install -e ".[dev]"

# Lint & format
ruff check .
ruff format .

# Tests (no API key needed — generator is mocked)
pytest tests/ -v
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |

Add to a `.env` file in the project root — `python-dotenv` loads it automatically.

## License

MIT — see [LICENSE](LICENSE).
