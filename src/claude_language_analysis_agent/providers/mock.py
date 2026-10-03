from claude_language_analysis_agent.agent import run_mock_agent

class MockProvider:
    def analyze(self, request: str, text: str) -> dict:
        trace = run_mock_agent(request, text)
        return {"tools_called": trace.tools_called, "tool_results": trace.tool_results}
