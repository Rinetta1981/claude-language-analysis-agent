from dataclasses import dataclass

from claude_language_analysis_agent.tools import analyze_text_features, compare_register_profile

@dataclass
class AgentTrace:
    request: str
    text: str
    tools_called: list[str]
    tool_results: dict

def choose_tools(request: str) -> list[str]:
    lowered = request.lower()
    selected = []
    if "register" in lowered or "tone" in lowered:
        selected.append("compare_register_profile")
    if "feature" in lowered or "polite" in lowered or "deadline" in lowered:
        selected.append("analyze_text_features")
    if not selected:
        selected = ["analyze_text_features", "compare_register_profile"]
    return selected

def run_mock_agent(request: str, text: str) -> AgentTrace:
    if not text.strip():
        raise ValueError("Text must not be empty.")
    tools = choose_tools(request)
    results = {}
    if "analyze_text_features" in tools:
        results["analyze_text_features"] = analyze_text_features(text)
    if "compare_register_profile" in tools:
        results["compare_register_profile"] = compare_register_profile(text)
    return AgentTrace(request, text, tools, results)
