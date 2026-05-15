from unittest.mock import patch

from fastapi.testclient import TestClient

from claude_md_gen.api import app

client = TestClient(app)


def test_index_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "CLAUDE.md Generator" in response.text


def test_generate_streams_content():
    with patch("claude_md_gen.api.stream_claude_md") as mock_gen:
        mock_gen.return_value = iter(["# My Project\n", "\nContent here.\n"])
        response = client.post(
            "/generate",
            json={"name": "my-project", "description": "A test project"},
        )
    assert response.status_code == 200
    assert "# My Project" in response.text
    assert "Content here." in response.text


def test_generate_accepts_all_fields():
    with patch("claude_md_gen.api.stream_claude_md") as mock_gen:
        mock_gen.return_value = iter(["# Done\n"])
        response = client.post(
            "/generate",
            json={
                "name": "full-app",
                "project_type": "CLI",
                "description": "Full field test",
                "stack": "Python",
                "commands": "pytest",
                "arch": "layered",
                "instructions": "be concise",
                "model": "claude-sonnet-4-6",
            },
        )
    assert response.status_code == 200
    mock_gen.assert_called_once()
    call_kwargs = mock_gen.call_args.kwargs
    assert call_kwargs["name"] == "full-app"
    assert call_kwargs["project_type"] == "CLI"
    assert call_kwargs["model"] == "claude-sonnet-4-6"


def test_generate_defaults_empty_fields():
    with patch("claude_md_gen.api.stream_claude_md") as mock_gen:
        mock_gen.return_value = iter(["ok"])
        response = client.post("/generate", json={})
    assert response.status_code == 200
