# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to change the existing single-call learning-path generator into a plan, generate, verify, and self-correct workflow. It had to use only retrieved opportunities, enforce four ordered stages with no more than three opportunities per stage, retry a rejected path at most twice, preserve the rule-based fallback, and expose a privacy-safe trace in the CLI and Streamlit UI. Scoring, guardrails, retrieval, and the dataset were out of scope.

**Prompts used:**

These are the prompt templates used by the workflow; the JSON placeholders are filled with the validated preferences, plan, retrieved items, and verifier errors for each run.

**Plan prompt template:**

```text
Create a short plan for a technology learning path. Return only valid JSON with one top-level "assignments" array. Each assignment must have exactly these keys: "title" (an exact retrieved title), "stage" (one of Foundations, Build Skills, Prove Skills, Apply), and "reason" (one concise sentence explaining the choice using learning preferences or opportunity type). Assign each retrieved opportunity at most once. Put internships and jobs in Apply when present. Do not invent titles or include any other fields.

Student learning preferences:
{profile_json}

Retrieved opportunities (the only allowed resources):
{retrieved_json}
```

**Generate prompt template:**

```text
Create a practical beginner-aware technology learning path using the plan as guidance. Return only valid JSON as an array of exactly four steps in this order: Foundations, Build Skills, Prove Skills, Apply. Every step must have exactly these keys: step_number (integer, 1 through 4), stage (string), goal (string), opportunity_titles (array of exact titles), and why (string). Use ONLY the retrieved opportunities; never invent or recommend resources, certifications, URLs, internships, or jobs. Each title may appear in only one stage, and each stage may contain at most 3 opportunities. Keep goals and reasons general; refer to specific resources only by listing their retrieved titles. {apply_instruction}

Student learning preferences:
{profile_json}

Agent plan:
{plan_json}

Retrieved opportunities (the only allowed resources):
{retrieved_json}
```

**Repair prompt template:**

```text
Correct the previous learning path so it passes every verifier check. Return only valid JSON as an array of exactly four steps in this order: Foundations, Build Skills, Prove Skills, Apply. Every step must have exactly these keys: step_number (integer, 1 through 4), stage (string), goal (string), opportunity_titles (array of exact titles), and why (string). Use ONLY the retrieved opportunities. Do not repeat a title across stages, and include at most 3 opportunities per stage. Address every verifier error listed below; keep the Apply step consistent with the retrieved internship/job data.

Verifier errors:
{errors_json}

Previous path output:
{previous_output}

Student learning preferences:
{profile_json}

Agent plan:
{plan_json}

Retrieved opportunities (the only allowed resources):
{retrieved_json}
```

**What did the agent generate or change?**

It updated `src/path_generator.py` with the agent steps, verification, two-repair limit, and trace; passed offline mode through `src/pipeline.py`; exposed traces in `src/main.py` and `app.py`; and added agent checks and repair-attempt reporting to `scripts/evaluate_reliability.py`. It added mocked workflow tests, `scripts/generate_agent_traces.py`, and the real trace evidence in [assets/agent_traces.md](assets/agent_traces.md). The real AI Engineering plan included: “This course builds essential Python and machine learning basics through a preferred free and remote format.”

**What did you verify or fix manually?**

The automated tests passed (46 tests), including mocked repair, stage-size, duplicate-title, offline, and API-key trace checks. In the latest online reliability run, the six preset-profile paths passed their checks and each used zero repairs; the run passed 66/67 checks overall. The Cloud consistency check measured 66.7% title overlap, below its 70% threshold. I reviewed the three saved real traces: each has PLAN, GENERATE, VERIFY, and DECIDE entries, passed verification on its first draft, and contains neither a full profile nor an API key. The traces and evaluation report are evidence for these runs, not a general quality guarantee.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
