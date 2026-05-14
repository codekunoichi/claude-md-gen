#!/usr/bin/env python3
"""CLI entry point for claude-md-gen."""

import argparse
import difflib
import sys
from pathlib import Path

from dotenv import load_dotenv

from claude_md_gen.generator import stream_claude_md

load_dotenv()

_RESET = "\033[0m"
_GREEN = "\033[32m"
_RED = "\033[31m"
_BOLD = "\033[1m"
_DIM = "\033[2m"


def _prompt(label: str, required: bool = False) -> str:
    while True:
        value = input(f"  {label}: ").strip()
        if value or not required:
            return value
        print("    (required — please enter a value)")


def _print_diff(old: str, new: str, path: str) -> None:
    diff = list(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"{path} (before)",
            tofile=f"{path} (after)",
        )
    )
    if not diff:
        print(f"\n{_DIM}No changes from the previous version.{_RESET}")
        return

    print(f"\n{_BOLD}Diff from previous version:{_RESET}")
    print("─" * 60)
    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            print(f"{_GREEN}{line}{_RESET}", end="")
        elif line.startswith("-") and not line.startswith("---"):
            print(f"{_RED}{line}{_RESET}", end="")
        else:
            print(line, end="")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="claude-md-gen",
        description="Generate a CLAUDE.md for your project using Claude AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  claude-md-gen                          # interactive mode\n"
            "  claude-md-gen --name myapp --type CLI  # flags mode\n"
        ),
    )
    parser.add_argument("--name", default="", metavar="NAME", help="Project name")
    parser.add_argument("--type", dest="project_type", default="", metavar="TYPE",
                        help="Project type (e.g. Web App, CLI, Library)")
    parser.add_argument("--description", default="", metavar="TEXT", help="What the project does")
    parser.add_argument("--stack", default="", metavar="STACK",
                        help="Tech stack (e.g. Python, FastAPI, PostgreSQL)")
    parser.add_argument("--commands", default="", metavar="CMDS", help="Key shell commands")
    parser.add_argument("--arch", default="", metavar="NOTES", help="Architecture notes")
    parser.add_argument("--instructions", default="", metavar="TEXT", help="Special Claude instructions")
    parser.add_argument("--output", default="CLAUDE.md", metavar="FILE",
                        help="Output file path (default: CLAUDE.md)")
    parser.add_argument("--model", default="claude-sonnet-4-6", metavar="MODEL",
                        help="Claude model to use")
    parser.add_argument("--no-interactive", action="store_true",
                        help="Disable interactive prompts (fail if required fields missing)")

    args = parser.parse_args()

    has_flags = any([
        args.name, args.project_type, args.description,
        args.stack, args.commands, args.arch, args.instructions,
    ])
    interactive = not args.no_interactive and not has_flags

    if interactive:
        print(f"\n{_BOLD}⚡ CLAUDE.md Generator{_RESET}\n")
        name = _prompt("Project name", required=True)
        project_type = _prompt("Project type (Web App, CLI, Library, API, …)")
        description = _prompt("What does it do?", required=True)
        stack = _prompt("Tech stack")
        commands = _prompt("Key commands (leave blank to skip)")
        arch = _prompt("Architecture notes (leave blank to skip)")
        instructions = _prompt("Special Claude instructions (leave blank to skip)")
    else:
        name = args.name
        project_type = args.project_type
        description = args.description
        stack = args.stack
        commands = args.commands
        arch = args.arch
        instructions = args.instructions

    output_path = Path(args.output)
    existing_content = output_path.read_text(encoding="utf-8") if output_path.exists() else None

    print(f"\n{_DIM}Generating with {args.model}…{_RESET}\n")
    print("─" * 60)

    chunks: list[str] = []
    try:
        for chunk in stream_claude_md(
            name=name,
            project_type=project_type,
            description=description,
            stack=stack,
            commands=commands,
            arch=arch,
            instructions=instructions,
            model=args.model,
        ):
            print(chunk, end="", flush=True)
            chunks.append(chunk)
    except RuntimeError as exc:
        print(f"\n{_RED}Error: {exc}{_RESET}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "─" * 60)

    generated = "".join(chunks)
    output_path.write_text(generated, encoding="utf-8")
    print(f"\n{_GREEN}✓{_RESET} Written to {_BOLD}{output_path}{_RESET}")

    if existing_content is not None:
        _print_diff(existing_content, generated, str(output_path))


if __name__ == "__main__":
    main()
