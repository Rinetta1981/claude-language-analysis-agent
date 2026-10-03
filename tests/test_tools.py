from claude_language_analysis_agent.tools import analyze_text_features, compare_register_profile

def test_polite_deadline_request():
    result = analyze_text_features("Could you please revise the report by Friday?")
    assert result["question_marks"] == 1
    assert "please" in result["polite_markers"]
    assert "could you" in result["polite_markers"]
    assert "by friday" in result["deadline_markers"]

def test_plain_statement():
    result = analyze_text_features("The report is complete.")
    assert result["question_marks"] == 0
    assert result["polite_markers"] == []
    assert result["deadline_markers"] == []

def test_institutional_register_profile():
    result = compare_register_profile("Pursuant to university policy, all applications shall be submitted by Friday.")
    assert result["best_match"] == "institutional"
    assert result["scores"]["institutional"] == 2

def test_unclear_register_profile():
    result = compare_register_profile("The document is on the table.")
    assert result["best_match"] == "unclear"
