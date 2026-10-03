"""Tests for ClaudeProvider that make zero real API calls."""

from types import SimpleNamespace

import pytest

from claude_language_analysis_agent.providers.claude import ClaudeProvider


class FakeMessages:
    def __init__(self) -> None:
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)

        if len(self.calls) == 1:
            return SimpleNamespace(
                content=[
                    SimpleNamespace(
                        type="tool_use",
                        id="tool_test_1",
                        name="compare_register_profile",
                        input={
                            "text": (
                                "Pursuant to university policy, "
                                "applications shall be submitted."
                            )
                        },
                    )
                ],
                stop_reason="tool_use",
            )

        return SimpleNamespace(
            content=[
                SimpleNamespace(
                    type="text",
                    text="The message has an institutional register profile.",
                )
            ],
            stop_reason="end_turn",
        )


class FakeClient:
    def __init__(self) -> None:
        self.messages = FakeMessages()


def test_claude_provider_runs_tool_loop_without_real_api_call():
    client = FakeClient()
    provider = ClaudeProvider(client=client, model="test-model")

    result = provider.analyze(
        "Assess the register.",
        "Pursuant to university policy, applications shall be submitted.",
    )

    assert result["model"] == "test-model"
    assert result["tools_called"] == ["compare_register_profile"]
    assert result["tool_results"]["compare_register_profile"]["best_match"] == "institutional"
    assert result["final_text"] == "The message has an institutional register profile."
    assert len(client.messages.calls) == 2


def test_claude_provider_rejects_empty_text_without_api_call():
    client = FakeClient()
    provider = ClaudeProvider(client=client, model="test-model")

    with pytest.raises(ValueError, match="Text must not be empty"):
        provider.analyze("Analyze this.", "   ")

    assert client.messages.calls == []


def test_claude_provider_requires_key_when_no_client(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY is not set"):
        ClaudeProvider()
