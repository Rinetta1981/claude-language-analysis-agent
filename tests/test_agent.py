from claude_language_analysis_agent.agent import run_mock_agent

def test_register_routing():
    trace = run_mock_agent("Assess the register.", "Pursuant to policy, applications shall be submitted.")
    assert trace.tools_called == ["compare_register_profile"]

def test_general_routing():
    trace = run_mock_agent("Analyze this workplace message.", "Could you please revise the report by Friday?")
    assert trace.tools_called == ["analyze_text_features", "compare_register_profile"]
