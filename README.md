# Claude Language Analysis Agent

A small, testable Python agent for workplace-language analysis with deterministic linguistic tools, provider abstraction, reproducible evaluation, and optional Claude API integration.

The project is designed to demonstrate applied AI engineering rather than to function as a production-ready sociolinguistic classifier.

## Why this project

Many small LLM demos send a prompt to a model and print the response. This repository takes a more auditable approach:

- separates deterministic feature extraction from model interpretation;
- exposes linguistic functions as callable tools;
- records which tools are selected;
- supports a free mock provider for local development and CI;
- includes an optional Claude provider with a client-side tool-use loop;
- evaluates routing and heuristic behavior on a frozen benchmark;
- runs automated tests and evaluation in GitHub Actions.

## What the agent analyzes

The current prototype focuses on workplace communication and exposes two tools:

### `analyze_text_features`

Extracts observable features such as:

- word count;
- question and exclamation marks;
- politeness markers;
- modal markers;
- deadline markers.

### `compare_register_profile`

Compares a message against a small, transparent heuristic inventory for:

- informal;
- neutral-professional;
- formal-professional;
- institutional;
- unclear.

These labels are heuristic outputs for the prototype. They are not presented as a validated sociolinguistic measurement instrument.

## Architecture

```text
User request + workplace message
              |
              v
        Agent / runner
              |
              v
     Provider abstraction
        /            \
       /              \
MockProvider        ClaudeProvider
 free/local         optional API
       \              /
        \            /
         Tool selection
          /        \
         v          v
analyze_text_    compare_register_
features()       profile()
         \          /
          \        /
           evidence
              |
              v
       structured result
              |
              v
     frozen evaluation
```

See [`docs/architecture.md`](docs/architecture.md) for more detail.

## Current evaluation

The frozen v0.1 benchmark contains 20 workplace-language cases.

| Metric | Result |
|---|---:|
| Execution success | 20/20 (100.0%) |
| Tool-routing accuracy | 20/20 (100.0%) |
| Heuristic register match | 13/14 (92.9%) |

These results were produced with `MockProvider`, not by making live Claude API calls.

The register metric measures agreement with the benchmark's frozen heuristic expectations. It does **not** establish construct validity or general sociolinguistic accuracy.

One observed mismatch illustrates a current limitation: phrases can activate markers from more than one register profile, while the simple scorer currently resolves ties through deterministic dictionary order rather than a learned or theoretically weighted decision rule.

Raw outputs and metrics are stored in:

```text
evaluation_results/mock_eval_raw_v0.1.json
evaluation_results/mock_eval_metrics_v0.1.json
```

## Repository structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── architecture.md
├── evaluation_results/
│   ├── mock_eval_metrics_v0.1.json
│   └── mock_eval_raw_v0.1.json
├── examples/
│   └── frozen_eval_v0.1.json
├── scripts/
│   ├── run_frozen_eval.py
│   └── score_frozen_eval.py
├── src/
│   └── claude_language_analysis_agent/
│       ├── agent.py
│       ├── providers/
│       │   ├── base.py
│       │   ├── claude.py
│       │   └── mock.py
│       ├── runner.py
│       ├── schemas.py
│       └── tools.py
├── tests/
│   ├── test_agent.py
│   ├── test_claude_provider.py
│   ├── test_providers.py
│   ├── test_schemas.py
│   └── test_tools.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Installation

Python 3.12 is recommended.

Create and activate an environment, then install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Run the tests

```bash
pytest -q
```

Current local result:

```text
13 passed
```

The Claude-provider tests use a fake client. They do not make external API requests.

## Run the frozen evaluation

```bash
python scripts/run_frozen_eval.py
python scripts/score_frozen_eval.py
```

The evaluation uses `MockProvider` and therefore does not require an Anthropic API key.

## Optional Claude API mode

The repository also contains a `ClaudeProvider` that implements a client-side tool-use loop.

To enable real API calls, set:

```bash
export ANTHROPIC_API_KEY="your_key_here"
```

Optionally override the configured model:

```bash
export ANTHROPIC_MODEL="your_model_id"
```

Never commit a real API key. `.env` is excluded by `.gitignore`.

A real API call may incur provider charges. The test suite, CI workflow, and frozen mock evaluation do not require paid API usage.

## Reproducibility

The benchmark is frozen in:

```text
examples/frozen_eval_v0.1.json
```

Execution and scoring are intentionally separated:

1. `scripts/run_frozen_eval.py` records observed behavior.
2. `scripts/score_frozen_eval.py` compares the saved observations with frozen expectations.

This prevents benchmark execution and scoring logic from being silently conflated.

## CI

GitHub Actions automatically:

1. sets up Python 3.12;
2. installs dependencies;
3. runs the test suite;
4. executes the frozen mock evaluation;
5. scores the evaluation.

No API key is required for CI.

## Current limitations

- register profiles use a deliberately small rule-based marker inventory;
- lexical matching does not model context, syntax, speaker relationships, or cultural variation;
- tie handling in the register heuristic is simplistic;
- the benchmark is small and implementation-oriented;
- the reported evaluation results apply to `MockProvider`, not live Claude behavior;
- the prototype does not claim sociolinguistic construct validation.

## Possible next extensions

- human-annotated evaluation data;
- multilingual workplace cases;
- weighted or learned register features;
- uncertainty estimates;
- richer failure analysis;
- optional live-provider benchmarking;
- structured final `LanguageAnalysis` generation from model outputs.

## Project goal

The repository demonstrates a compact applied-AI workflow combining:

**linguistic expertise + tool-using agent design + provider abstraction + automated testing + reproducible evaluation.**
