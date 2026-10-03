from claude_language_analysis_agent.schemas import LanguageAnalysis

def test_valid_analysis():
    result = LanguageAnalysis(register_label="neutral-professional", directness=4, politeness=4, ambiguity=1, evidence=["Please"])
    assert result.directness == 4
