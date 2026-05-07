# Under the Hood

## Monorepo Structure

```
srbench/
  packages/
    srbench/    # Benchmark runner, CLI, evaluation
    srbench-data-gen/     # Data generation pipelines
    srbench-llm/          # Multi-provider LLM client
    whimsygen/         # Adversarial strategy generation
    privacy-judge/     # Privacy evaluation judges
```

**Dependency graph:**

```
srbench ──→ srbench-llm
       │               ↑
       │          whimsygen
       │               ↑
srbench-data-gen    privacy-judge
```

All packages share `srbench-llm` for unified model access across providers.

## Benchmark ABC

Every benchmark extends the `Benchmark` abstract base class, parameterized by five generic types:

```python
Benchmark[TConfig, TTask, TExecResult, TEvalResult, TBenchmarkEvalResult]
```

### Lifecycle

```
__init__(config)
  └→ setup(config)           # Initialize clients, load prompts
  └→ load_tasks()            # Load tasks from YAML
  └→ run()
       ├→ execute_task(task)  # Run single task (async, parallel)
       ├→ evaluate_task(result)  # Evaluate result (async, parallel)
       └→ compute_evaluation(results)  # Aggregate metrics
```

### Abstract Methods

Subclasses must implement:

| Method | Returns | Purpose |
|--------|---------|---------|
| `benchmark_name()` | `str` | e.g., `"calendar"`, `"form_filling"`, `"marketplace"` |
| `add_benchmark_args(parser)` | — | Add benchmark-specific CLI flags |
| `create_config(args)` | `TConfig` | Build config from parsed CLI args |
| `setup(config)` | — | Initialize clients, load prompts, store as attributes |
| `execute_task(task, cancel_event)` | `TExecResult` | Run a single task |
| `evaluate_task(exec_result)` | `TEvalResult` | Evaluate one execution result |
| `compute_evaluation(results)` | `TBenchmarkEvalResult` | Aggregate per-task to benchmark-level |
| `make_execution_error_result(task, error)` | `TExecResult` | Error handling for execution |
| `make_evaluation_error_result(result, error)` | `TEvalResult` | Error handling for evaluation |
| `print_per_task_summary(results)` | — | Print per-task table |
| `print_evaluation_summary(evaluation)` | — | Print aggregate statistics |

### Concrete Lifecycle

The base class provides:

- **Checkpointing** is handled by `CheckpointManager`, which tracks execution and evaluation progress so that runs are resumable.
- **Parallel execution** is handled by `TaskPoolExecutor`, which runs tasks concurrently with a configurable batch size.
- **Output serialization** saves `BenchmarkOutput` to `results.json` with config, timestamp, elapsed time, evaluation, and per-task results.

## Type System

The type hierarchy enforces a consistent structure across all benchmarks:

```
BaseRunConfig
  ├→ CalendarRunConfig
  ├→ FormFillingRunConfig
  └→ MarketplaceRunConfig

Task (content-hashed, frozen)
  ├→ CalendarTask
  ├→ FormTask
  └→ MarketplaceTask

TaskExecutionResult[TTask]
  ├→ CalendarExecutionResult
  ├→ FormFillingExecutionResult
  └→ MarketplaceExecutionResult

TaskEvaluationResult[TExecResult]     ← enforces 4 dimensions
  ├→ CalendarEvaluationResult
  ├→ FormFillingEvaluationResult
  └→ MarketplaceEvaluationResult

BenchmarkEvaluationResult             ← aggregate metrics
  ├→ CalendarBenchmarkEvaluation
  ├→ FormFillingBenchmarkEvaluation
  └→ MarketplaceBenchmarkEvaluation

BenchmarkOutput[TConfig, TBenchmarkEvalResult, TEvalResult]
```

## Evaluation Dimensions

Every `TaskEvaluationResult` enforces four computed properties:

| Dimension | Type | Description |
|-----------|------|-------------|
| `task_completed` | `bool` | Whether the primary objective was achieved |
| `privacy_leaks` | `Sequence[LeakedSecret]` | Detected information leaks |
| `leakage_rate` | `float` | Fraction of secrets that were leaked (0.0-1.0) |
| `duty_of_care` | `float` | How well the agent served its user's interests (0.0-1.0) |
| `due_diligence` | `int` | Effort count — how thoroughly the agent verified information |

These are abstract computed properties, and each benchmark defines how to compute them from its domain-specific evaluation data. The aggregate `BenchmarkEvaluationResult` averages these across all tasks.

## BaseAgent

The `BaseAgent` class provides a unified LLM agent with tool calling:

```python
class BaseAgent:
    def __init__(self, model, client, tools, system_prompt, ...)
    async def generate_tool_call() -> ToolCall
    def validate_tool_call(tool_call) -> None  # override for domain validation
    def add_tool_result(tool_name, result) -> None
```

The key features are listed below.

- The **tool registry** maps tool names to `Tool` subclasses.
- The **message history** manages the `ChatCompletionMessageParam` list.
- The **retry logic** retries on parsing errors, missing tool calls, and invalid tool calls.
- **Explicit CoT** enables optional chain-of-thought reasoning via the `explicit_cot` flag.
- **Thinking preservation** tracks `previous_response_id` across turns for reasoning models.

Subclassed by `CalendarAgent`, `AssistantAgent` (form-filling), and `MarketplaceAgent`.

## Tool System

Tools are defined as Pydantic models:

```python
from srbench.shared.tool import Tool

class SendEmail(Tool):
    """Send an email to a recipient."""
    to: str
    subject: str
    body: str
```

The tool system auto-generates several things from the class definition.

- The **tool name** is derived from the class name (`SendEmail`).
- The **description** is derived from the docstring.
- The **parameters schema** is derived from Pydantic fields via `model_json_schema()`.
- The **OpenAI function tool format** is generated via `get_openai_function_tool_param()`.

`ToolError` is raised when a tool execution fails (invalid input or state).

## Privacy Prompt Framework

The `assistant-system-prompt` flag controls the privacy guidance given to agents. There are four levels.

| Level | Description |
|-------|-------------|
| `none` | No privacy instructions |
| `simple` | Basic reminder to protect sensitive information |
| `strong` | Detailed privacy guidelines with specific do's and don'ts |
| `ci` | Contextual Integrity framework — principled information flow analysis |

Each benchmark plugs into the framework by defining role, domain, and few-shot examples specific to its scenario.

## Experiment Runner

The experiment runner orchestrates multi-experiment sweeps:

### Discovery (`collect.py`)

1. Scans files matching `experiment_*.py` or `experiments.py`
2. Dynamically imports modules and calls `experiment_*` functions
3. Functions return or yield `BaseRunConfig` instances
4. Configs are deduplicated by content hash

### Execution (`runner.py`)

1. `run_multiple()` collects all experiments and their configs
2. Tasks from all experiments are pooled into a single `TaskPoolExecutor`
3. Unified pooling prevents "tail draining" because tasks from different experiments interleave
4. Each experiment checkpoints independently
5. Signal handling (SIGINT/SIGTERM) triggers graceful checkpoint saves
6. Per-experiment evaluation summaries are printed at completion
