"""Provider-independent entry point for language analysis.

This module does not select a provider or make API calls itself. The caller
supplies a backend implementing LanguageModelProvider.analyze().
"""

from claude_language_analysis_agent.providers.base import LanguageModelProvider


def run_agent(
    request: str,
    text: str,
    provider: LanguageModelProvider,
) -> dict:
    """Delegate analysis to the supplied provider and return its result.

    Validation and execution are the provider's responsibility. Provider
    exceptions propagate to the caller; this function does not hide failures.
    """
    return provider.analyze(request, text)
