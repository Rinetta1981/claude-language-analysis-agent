import re

def analyze_text_features(text: str) -> dict:
    lowered = text.lower()
    words = re.findall(r"\b\w+\b", text)

    polite_markers = ["please", "could you", "would you", "would you mind", "thank you"]
    modal_markers = ["could", "would", "might", "may", "should"]
    deadline_markers = ["today", "tomorrow", "by monday", "by friday", "as soon as possible", "asap"]

    return {
        "word_count": len(words),
        "question_marks": text.count("?"),
        "exclamation_marks": text.count("!"),
        "polite_markers": [marker for marker in polite_markers if marker in lowered],
        "modal_markers": [marker for marker in modal_markers if marker in lowered],
        "deadline_markers": [marker for marker in deadline_markers if marker in lowered],
    }

def compare_register_profile(text: str) -> dict:
    lowered = text.lower()

    profiles = {
        "informal": ["hey", "cheers", "gonna", "wanna", "no worries"],
        "neutral-professional": ["please", "could you", "would you", "thank you"],
        "formal-professional": ["kindly", "would appreciate", "at your earliest convenience", "please be advised"],
        "institutional": ["pursuant to", "in accordance with", "hereby", "shall"],
    }

    scores = {
        profile: sum(marker in lowered for marker in markers)
        for profile, markers in profiles.items()
    }

    best_match = max(scores, key=scores.get)

    if scores[best_match] == 0:
        best_match = "unclear"

    return {
        "best_match": best_match,
        "scores": scores,
    }
