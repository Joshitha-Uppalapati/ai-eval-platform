# Production-Grade AI Evaluation & Data Intelligence Platform

This project is a minimal, structured system for running, tracking, and comparing machine learning experiments.
The focus is on **reproducibility and clarity**, not model complexity.

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

The system scales naturally as more experiments are added.

---

## What this system does
- Runs experiments driven by configuration files.
- Creates a unique folder for each run.
- Stores config and metrics per run.
- Lists and compares past runs.
- Exports all results to a CSV for analysis.

The CSV is **derived output**, not the source of truth.

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

## How experiments work
1. `run.py` reads parameters from a config file
2. A new run directory is created with a timestamp ID
3. The config used for the run is copied into the run folder
4. Metrics are computed and saved as `metrics.json`
5. Each run is fully traceable and reproducible

Changing the config produces a new, comparable run.

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
