# Building with Claude — Learning Materials

## Overview
- **Purpose:** A compact lesson-plan collection demonstrating Anthropic/Claude API usage patterns: simple requests, system prompts, streaming, structured output, tool-driven workflows, and evaluation.
- **Audience:** Instructors, learners, and engineers experimenting with LLM-driven tools, evaluation workflows, and structured-data handling.

## Quick start
- **Prereqs:** Python 3.8+, the `anthropic` client, and `python-dotenv` (or your preferred environment variable manager).
- **Run examples:**

```bash
python api_capabilities/001_requests.py
python api_capabilities/002_system_prompts.py
python api_capabilities/003_streaming.py
python api_capabilities/004_structured_data.py
python api_capabilities/005_ctrl_model_output.py
python tool_use/tool_use.py
```

## Lesson plans & files
- **Basics — Simple chat loop:** `api_capabilities/001_requests.py` — Intro to `client.messages.create`, building message lists, and a simple interactive loop.
- **System prompts & temperature:** `api_capabilities/002_system_prompts.py` — Demonstrates `system` prompts and varying `temperature` to shape responses.
- **Streaming responses:** `api_capabilities/003_streaming.py` — Shows streaming API usage and how to consume partial outputs in real time.
- **Structured output & stop sequences:** `api_capabilities/004_structured_data.py` — Message prefilling, stop sequences, and parsing generated JSON robustly.
- **Evaluation & grading workflow:** `api_capabilities/005_ctrl_model_output.py` — Dataset generation, prompt runners, syntax validators, and model-based grading; produces `eval_results.json`.
- **Tool-driven interactions:** `tool_use/tool_use.py` — Example tools such as `get_current_datetime`, `add_duration_to_datetime`, `set_reminder`, and a tool-use conversation loop demonstrating orchestration patterns.
- **Structured-data helper schemas:** `tool_use/tools_for_structured_data.py` — Example schemas and helpers for tool inputs and structured outputs.
- **Prompt evaluation & reporting:** `prompts/006_eval_workflow.py` and `prompts/007_prompt_engineering_techniques.py` — Test-case generation, `PromptEvaluator` utilities, and HTML report generation (`output.html`).

## Data & outputs
- **Seed files:** `dataset.json`, `generated_dataset.json`
- **Results artifacts:** `eval_results.json`, `output.json`, `output.html`

## Teaching activities (suggested exercises)
- **Activity 1 (Beginner):** Run `api_capabilities/001_requests.py`, change a system prompt, and observe output differences when adjusting `temperature`.
- **Activity 2 (Intermediate):** Extend `tool_use/tool_use.py` with a new tool (e.g., `convert_timezone`) and write a conversation that triggers it.
- **Activity 3 (Advanced):** Add a new test-case generator in `prompts/007_prompt_engineering_techniques.py`, run the evaluation pipeline, and iterate prompts based on the HTML report.
- **Activity 4 (Assessment):** Enhance the grader in `api_capabilities/005_ctrl_model_output.py` with an additional rubric (for example, safety or factuality) and re-run `run_eval`.

## Tips
- Keep API keys and secrets out of source control. Use environment variables or a `.env` file loaded by `python-dotenv`.
- When parsing model outputs, validate JSON and handle partial/streamed responses defensively.

## Next steps
- Run the example scripts to generate `output.html` and `eval_results.json`, then iterate prompts and tools as classroom exercises.

---

If you want, I can also add a `requirements.txt` and a short `RUN.md` with commands to create a virtual environment and install dependencies.
