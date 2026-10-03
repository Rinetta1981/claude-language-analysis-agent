"""Offline tests of the provider interface and application entry point.

These tests check software behavior, not Claude performance or the validity
of the heuristic tools as sociolinguistic measurements. No API key is needed.
"""

import pytest

from claude_language_analysis_agent.providers.mock import MockProvider
from claude_language_analysis_agent.runner import run_agent


def test_mock_provider_returns_register_trace() -> None:
    """The entry point should preserve the mock provider's tool trace."""
    result = run_agent(
        request="Assess the register.",
        text="Pursuant to policy, applications shall be submitted.",
        provider=MockProvider(),
    )

    assert result["tools_called"] == ["compare_register_profile"]
    profile = result["tool_results"]["compare_register_profile"]
    assert profile["best_match"] == "institutional"
    assert profile["scores"]["institutional"] == 2


def test_entry_point_accepts_another_provider() -> None:
    """A second backend can be supplied without changing run_agent()."""
    calls: list[tuple[str, str]] = []
    expected = {"tools_called": [], "tool_results": {}}

    class RecordingProvider:
        """Record calls locally; this is a test double, not a model."""

        def analyze(self, request: str, text: str) -> dict:
            calls.append((request, text))
            return expected

    result = run_agent(
        request="Analyze this message.",
        text="The report is ready.",
        provider=RecordingProvider(),
    )

    assert calls == [("Analyze this message.", "The report is ready.")]
    assert result is expected


def test_mock_provider_rejects_empty_text() -> None:
    """The application entry point must not swallow validation errors."""
    with pytest.raises(ValueError, match=r"^Text must not be empty\.$"):
        run_agent(
            request="Analyze this message.",
            text="   ",
            provider=MockProvider(),
        )
