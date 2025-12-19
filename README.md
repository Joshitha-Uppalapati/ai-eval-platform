# Production-Grade AI Evaluation & Data Intelligence Platform

## System Overview
This project is a local, reproducible system for running and comparing machine learning evaluation experiments.
Each experiment is executed with an explicit configuration, produces structured outputs, and is stored under a unique run ID.
Metrics, judge signals, and decisions are logged per run and aggregated for comparison. The system is deterministic, self-contained, and designed to run fully offline. Its goal is to make AI evaluation **reliable**, **inspectable**, and **enforceable**, not just measurable.

The focus is on reproducibility and decision quality, not model complexity.

---

## The problem this project solves
In real ML and LLM systems, results are often hard to trust because:
- configurations change without being recorded
- metrics are inspected manually instead of enforced
- “good enough” outputs silently reach production
- evaluation logic lives in notebooks instead of systems
Accuracy alone is not sufficient for reliable AI systems.
This project treats evaluation as a first-class system concern, with explicit decision gates and traceability.

---

## What this system does
- Runs experiments driven by configuration files
- Creates an isolated folder for each run
- Stores frozen configs, metrics, and decisions per run
- Applies a **PASS / FAIL / REVIEW** decision policy
- Supports **LLM-as-a-Judge** (mocked locally)
- Enforces quality gates via CI
- Exports results for comparison and analysis

The CSV is derived output, not the source of truth.

---
## System Architecture
A single experiment flows through the system as follows:

```text
Config (YAML)
   ↓
src/run.py
   ↓
Golden Dataset + Evaluation Logic
   ↓
LLM-as-Judge (mocked)
   ↓
Decision Policy (PASS / FAIL / REVIEW)
   ↓
runs/<run_id>/
   ├─ config.yaml
   ├─ metrics.json
   └─ decision metadata
   ↓
CI / Analysis / API
```

Each run is isolated and fully traceable.
Changing any input always produces a new, comparable run.

---

## Golden Dataset
data/dataset.csv is the Golden Dataset for this project.
It is a small, fixed dataset checked into the repository and used to:
- validate end-to-end execution
- ensure metric stability
- catch regressions automatically in CI

The Golden Dataset is intentionally simple so results are deterministic across environments.

---

## Decision Policy
Every run is labeled using a versioned decision policy:
- **PASS** - metrics and judge signals meet acceptance thresholds
- **FAIL** - metrics or judge signals fall below minimum thresholds
- **REVIEW** - mixed signals that require human inspection
This mirrors how real AI systems gate deployments.

---

## Continuous Integration (CI)
This project includes a lightweight CI pipeline that runs a mini evaluation on every push.
CI exists to enforce correctness and prevent regressions, not to benchmark performance:
- experiments must run end-to-end
- metrics must be computed and logged
- decision logic must remain consistent
- regressions fail fast
CI uses the Golden dataset and a mock judge to remain fast, local, and predictable.

---

## Example Run
```text
Run ID: 20251218_183205
Accuracy: 1.00
Judge score: 1.00
Decision: PASS

Reason:
High agreement between predictions and references,
validated by both deterministic metrics and judge evaluation.
```

---

## Project structure
```text
ai-eval-platform/
├── api/              
├── configs/
├── data/
├── evaluation/
├── src/
├── tests/
├── runs/
├── experiments.csv
├── README.md
└── .github/workflows/
```

---

## Running an experiment
```bash
python3 -m src.run
```
## Running Tests
```bash
pytest
```
## Running the API
```bash
python3 -m uvicorn api.main:app --reload
```

---

## Design Decisions
- Golden Dataset ensures deterministic validation
- Mock judge enables fast, offline CI
- Decision policy is versioned to support future evolution
- Metrics are stored, not printed, to support auditability

---

## Limitations & Assumptions
- This is not a benchmarking suite
- CI is not meant for performance comparison
- Mock judge ≠ real LLM judge
- Designed for reliability experiments, not model training

---

## Final Outcome
At the end of this project, you have:
- a reproducible AI evaluation system
- explicit quality gates for AI outputs
- CI-enforced reliability checks
- a clean, inspectable experiment history
This is an AI reliability system, not just an experiment script

---

## API Interface
This platform exposes a local FastAPI service for triggering experiments and retrieving evaluation results programmatically.
This enables integration with other systems or automation pipelines.
This platform exposes a local FastAPI service for triggering experiments and retrieving evaluation results programmatically.
