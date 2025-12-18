# Production-Grade AI Evaluation & Data Intelligence Platform

## System Overview
This project is a local, reproducible system for running and comparing machine learning evaluation experiments.
Each experiment is executed with an explicit configuration, produces structured outputs, and is stored under a unique run ID.
Metrics and metadata are logged per run and can be aggregated for comparison and analysis.
The system is deterministic, self-contained, and fully runnable on local machines.
Its primary goal is to support reliable experiment evaluation without relying on external services.

The focus is on reproducibility and clarity, not model complexity.

---

## Why this project exists
In many ML projects, results are difficult to trust because:
- configurations change without being recorded
- metrics are copied manually
- it’s unclear how a result was produced

This project solves that by treating each experiment run as a first-class object with:
- a unique run ID
- a frozen configuration
- recorded metrics
- structured outputs

As a result, experiments are traceable, comparable, and reproducible by default.

---

## What this system does
- Runs experiments driven by configuration files.
- Creates a unique folder for each run.
- Stores configuration and metrics per run.
- Lists and compares past runs.
- Exports all results to a CSV for analysis.

The CSV is **derived output**, not the source of truth.

---
## System Architecture
A single experiment flows through the system as follows:

```text
Config (YAML)
   ↓
src/run.py
   ↓
Data + Evaluation Logic
   ↓
runs/<run_id>/
   ├─ config.yaml
   ├─ metrics.json
   └─ metadata.json
   ↓
src/export_csv.py / analysis scripts
   ↓
experiments.csv / analysis outputs
```

Each run is isolated and fully traceable.
Changing the configuration always produces a new, comparable run.

---

## Golden Dataset
The file data/dataset.csv is the Golden Dataset for this project.
It is a small, fixed dataset checked into the repository and used to:
- Validate end-to-end experiment execution
- Ensure metric computation is stable
- Catch regressions during automated testing
The Golden Dataset is intentionally simple so results are deterministic across environments.

---

## Continuous Integration (CI)
This project includes a lightweight CI pipeline that runs a mini evaluation on every push.
CI exists to enforce correctness, not performance benchmarking:
- Experiments must still run end-to-end
- Metrics must be computed and logged correctly
- Regressions should fail fast
CI uses the Golden Dataset to keep validation fast and predictable.

---

## How experiments work
1. `run.py` reads parameters from a config file
2. A new run directory is created with a timestamp ID
3. The config used for the run is copied into the run folder
4. Metrics are computed and saved as `metrics.json`
5. Each run is fully traceable and reproducible

Changing the config produces a new, comparable run.

---

```md
# Project structure
ai-eval-platform/
├── configs/
│ └── default.yaml
├── src/
│ ├── run.py
│ ├── list_runs.py
│ └── export_csv.py
├── runs/ # per-run outputs (git-ignored)
├── experiments.csv # generated summary
├── README.md
└── .gitignore
```

---

## Running an experiment
```bash
python3 src/run.py
```
## Listing past runs
```bash
python3 src/list_runs.py
```
## Exporting results to CSV
```bash
python3 src/export_csv.py
```

---

## API Interface
This platform exposes a local FastAPI service for triggering experiments and retrieving evaluation results programmatically.
