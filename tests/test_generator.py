
from claude_md_gen.generator import build_user_prompt


def test_build_user_prompt_all_fields():
    prompt = build_user_prompt(
        name="ink-to-calendar",
        project_type="Web App",
        description="Photographs handwritten planner and schedules tasks",
        stack="Python, FastAPI, SQLite",
        commands="python main.py",
        arch="Two-env config with symlink pattern",
        instructions="Always verify which env is active",
    )
    assert "ink-to-calendar" in prompt
    assert "Web App" in prompt
    assert "Python, FastAPI, SQLite" in prompt
    assert "python main.py" in prompt
    assert "Always verify which env is active" in prompt


def test_build_user_prompt_skips_empty_fields():
    prompt = build_user_prompt(
        name="minimal",
        project_type="",
        description="Does one thing well",
        stack="",
        commands="",
        arch="",
        instructions="",
    )
    assert "minimal" in prompt
    assert "Does one thing well" in prompt
    assert "Tech Stack" not in prompt
    assert "Key Commands" not in prompt
    assert "Architecture Notes" not in prompt
    assert "Special Claude Instructions" not in prompt


def test_build_user_prompt_returns_string():
    result = build_user_prompt("x", "y", "z", "", "", "", "")
    assert isinstance(result, str)
    assert len(result) > 0
