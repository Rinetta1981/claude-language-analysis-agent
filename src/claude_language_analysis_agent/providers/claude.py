"""Claude API provider with client-side tool use.

This module is safe to unit-test without an API key by injecting a fake client.
A real API call occurs only when ClaudeProvider is instantiated without a client
and analyze() is called with a valid ANTHROPIC_API_KEY.
"""

from __future__ import annotations

import json
import os
from typing import Any

from anthropic import Anthropic

from claude_language_analysis_agent.tools import (
    analyze_text_features,
    compare_register_profile,
)


TOOLS = [
    {
        "name": "analyze_text_features",
        "description": (
            "Extract observable linguistic features from a workplace message, "
            "including politeness markers, modal markers, deadlines, punctuation, "
            "and word count."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The workplace message to analyze.",
                }
            },
            "required": ["text"],
        },
    },
    {
        "name": "compare_register_profile",
        "description": (
            "Compare a workplace message against simple register profiles and "
            "return heuristic evidence for informal, neutral-professional, "
            "formal-professional, institutional, or unclear register."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The workplace message to compare.",
                }
            },
            "required": ["text"],
        },
    },
]


def _run_tool(name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    text = str(tool_input.get("text", ""))

    if name == "analyze_text_features":
        return analyze_text_features(text)

    if name == "compare_register_profile":
        return compare_register_profile(text)

    raise ValueError(f"Unknown tool: {name}")


class ClaudeProvider:
    """Run a small Claude tool-use loop for language analysis."""

    def __init__(
        self,
        client: Any | None = None,
        model: str | None = None,
        max_tokens: int = 700,
        max_tool_rounds: int = 3,
    ) -> None:
        if client is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY is not set. "
                    "Use MockProvider for free local runs."
                )
            client = Anthropic(api_key=api_key)

        self.client = client
        self.model = model or os.getenv(
            "ANTHROPIC_MODEL",
            "claude-sonnet-5-5",
        )
        self.max_tokens = max_tokens
        self.max_tool_rounds = max_tool_rounds

    def analyze(self, request: str, text: str) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Text must not be empty.")

        messages: list[dict[str, Any]] = [
            {
                "role": "user",
                "content": (
                    f"{request}\n\n"
                    f"Workplace message:\n{text}\n\n"
                    "Use the available linguistic tools when they provide useful "
                    "evidence. After tool use, give a concise evidence-grounded "
                    "analysis."
                ),
            }
        ]

        tools_called: list[str] = []
        tool_results: dict[str, Any] = {}

        for _ in range(self.max_tool_rounds + 1):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                tools=TOOLS,
                tool_choice={"type": "auto"},
                messages=messages,
            )

            tool_uses = [
                block
                for block in response.content
                if getattr(block, "type", None) == "tool_use"
            ]

            if not tool_uses:
                final_text = "\n".join(
                    block.text
                    for block in response.content
                    if getattr(block, "type", None) == "text"
                ).strip()

                return {
                    "model": self.model,
                    "tools_called": tools_called,
                    "tool_results": tool_results,
                    "final_text": final_text,
                }

            result_blocks = []

            for block in tool_uses:
                result = _run_tool(block.name, block.input)
                tools_called.append(block.name)
                tool_results[block.name] = result
                result_blocks.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": result_blocks})

        raise RuntimeError("Claude exceeded the maximum number of tool rounds.")
