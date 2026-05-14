"""FastAPI web interface for claude-md-gen."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from claude_md_gen.generator import stream_claude_md

load_dotenv()

app = FastAPI(
    title="CLAUDE.md Generator",
    description="Generate production-quality CLAUDE.md files using Claude AI",
    version="0.1.0",
)

_STATIC = Path(__file__).parent.parent / "static"


class GenerateRequest(BaseModel):
    name: str = ""
    project_type: str = ""
    description: str = ""
    stack: str = ""
    commands: str = ""
    arch: str = ""
    instructions: str = ""
    model: str = "claude-sonnet-4-6"


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html_file = _STATIC / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>CLAUDE.md Generator</h1><p>Run from repo root so static/ is found.</p>")


@app.post("/generate")
async def generate(req: GenerateRequest) -> StreamingResponse:
    def _stream():
        yield from stream_claude_md(
            name=req.name,
            project_type=req.project_type,
            description=req.description,
            stack=req.stack,
            commands=req.commands,
            arch=req.arch,
            instructions=req.instructions,
            model=req.model,
        )

    return StreamingResponse(_stream(), media_type="text/plain; charset=utf-8")


def start() -> None:
    import uvicorn
    uvicorn.run("claude_md_gen.api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
