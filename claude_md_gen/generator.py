import os
from collections.abc import Iterator

import anthropic

SYSTEM_PROMPT = """\
You are an expert at writing CLAUDE.md files for software projects.

CLAUDE.md lives in the repository root and gives Claude Code instant context — commands to run, \
architecture patterns, conventions, and any special AI instructions. It is read at the start of \
every Claude Code session.

Write a production-quality CLAUDE.md based on the project details provided. Rules:
- Be concise and direct — every line should earn its place
- Use ## headings to organize sections
- Include a quick "Key Commands" section with runnable shell commands in code fences
- Capture architecture decisions that aren't obvious from reading the code
- End with a "Special Claude Instructions" section if any were provided
- Do NOT include placeholder text or TODO sections
- Output only the Markdown content, no preamble
"""


def build_user_prompt(
    name: str,
    project_type: str,
    description: str,
    stack: str,
    commands: str,
    arch: str,
    instructions: str,
) -> str:
    parts = ["Generate a CLAUDE.md for this project:\n"]
    if name:
        parts.append(f"**Project Name:** {name}")
    if project_type:
        parts.append(f"**Type:** {project_type}")
    if description:
        parts.append(f"**What it does:** {description}")
    if stack:
        parts.append(f"**Tech Stack:** {stack}")
    if commands:
        parts.append(f"**Key Commands:**\n{commands}")
    if arch:
        parts.append(f"**Architecture Notes:** {arch}")
    if instructions:
        parts.append(f"**Special Claude Instructions:** {instructions}")
    return "\n".join(parts)


def stream_claude_md(
    name: str = "",
    project_type: str = "",
    description: str = "",
    stack: str = "",
    commands: str = "",
    arch: str = "",
    instructions: str = "",
    model: str = "claude-sonnet-4-6",
) -> Iterator[str]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")

    client = anthropic.Anthropic(api_key=api_key)
    user_prompt = build_user_prompt(name, project_type, description, stack, commands, arch, instructions)

    with client.messages.stream(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        yield from stream.text_stream
