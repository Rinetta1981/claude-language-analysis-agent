# Architecture

## 1. Design objective

The project separates four concerns that are often collapsed in small LLM demos:

1. **task routing** — deciding which capability is relevant;
2. **deterministic tools** — extracting transparent linguistic evidence;
3. **provider integration** — choosing a free mock backend or optional Claude backend;
4. **evaluation** — recording and scoring behavior against a frozen benchmark.

This separation keeps the system testable without requiring live API calls.

## 2. High-level flow

```text
User
 |
 | request + workplace message
 v
Runner / agent
 |
 v
Provider interface
 |-------------------------------|
 v                               v
MockProvider                ClaudeProvider
 |                               |
 | deterministic routing         | model-mediated tool choice
 |                               |
 |-------------------------------|
                 |
                 v
          Linguistic tools
          /              \
         v                v
analyze_text_features   compare_register_profile
         \                /
          \              /
             evidence
                 |
                 v
              result
                 |
                 v
         frozen evaluation
```

## 3. Agent routing

`agent.py` contains the free deterministic routing layer used by `MockProvider`.

Examples:

- register/tone request -> `compare_register_profile`
- politeness/deadline/feature request -> `analyze_text_features`
- broad analysis request -> both tools

This routing logic is deliberately simple so that expected behavior can be frozen and tested.

## 4. Linguistic tools

### `analyze_text_features`

Returns observable surface features, including:

- word count;
- punctuation counts;
- matched politeness expressions;
- modal markers;
- deadline expressions.

### `compare_register_profile`

Scores a small lexical marker inventory across four profiles:

- informal;
- neutral-professional;
- formal-professional;
- institutional.

If no marker is matched, the result is `unclear`.

This is a heuristic component, not a validated sociolinguistic classifier.

## 5. Provider abstraction

`providers/base.py` defines the expected provider interface.

Two implementations are included:

### `MockProvider`

- free;
- deterministic;
- suitable for tests and CI;
- used for the frozen v0.1 benchmark.

### `ClaudeProvider`

- optional;
- requires an API key only for live calls;
- exposes the linguistic functions as tools;
- receives tool-use requests;
- executes the requested local function;
- returns the tool result to the model;
- continues until a final text response is produced or the tool-round limit is reached.

The Claude provider is unit-tested with an injected fake client, so automated tests do not contact an external API.

## 6. Evaluation architecture

The benchmark is stored separately from both execution and scoring:

```text
examples/frozen_eval_v0.1.json
        |
        v
scripts/run_frozen_eval.py
        |
        v
evaluation_results/mock_eval_raw_v0.1.json
        |
        v
scripts/score_frozen_eval.py
        |
        v
evaluation_results/mock_eval_metrics_v0.1.json
```

This separation makes it easier to audit:

- what was expected;
- what the system actually did;
- how metrics were calculated.

## 7. Current v0.1 results

For the 20-case frozen mock benchmark:

- execution success: 20/20 (100.0%);
- routing accuracy: 20/20 (100.0%);
- heuristic register match: 13/14 (92.9%).

The results describe deterministic implementation behavior. They do not demonstrate general sociolinguistic validity or live-Claude performance.

## 8. Failure analysis

The current register scorer uses simple marker counts. A phrase such as `please be advised` can contain both:

- `please`, associated with the neutral-professional profile; and
- `please be advised`, associated with the formal-professional profile.

When scores tie, the current implementation resolves the result through deterministic dictionary order. This explains one frozen-benchmark mismatch and identifies a concrete target for later improvement.

## 9. Safety and cost boundary

The default reproducible workflow uses `MockProvider`.

No Anthropic API key is required for:

- local tests;
- the frozen benchmark;
- scoring;
- GitHub Actions CI.

Live Claude usage is optional and may incur external API charges.
