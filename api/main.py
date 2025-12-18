from fastapi import FastAPI, HTTPException
from pathlib import Path
import json
import subprocess

app = FastAPI(title="AI Evaluation Platform")

RUNS_DIR = Path("runs")


@app.post("/run")
def run_experiment():
    try:
        result = subprocess.run(
            ["python3", "-m", "src.run"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)

    # Extract latest run_id
    run_ids = sorted([p.name for p in RUNS_DIR.iterdir() if p.is_dir()])
    run_id = run_ids[-1]

    metrics_path = RUNS_DIR / run_id / "metrics.json"
    with open(metrics_path) as f:
        metrics = json.load(f)

    return {
        "run_id": run_id,
        "decision": metrics["decision"],
        "accuracy": metrics["accuracy"],
        "judge_score": metrics["judge_score"],
    }


@app.get("/runs")
def list_runs():
    runs = []
    for run_dir in sorted(RUNS_DIR.iterdir()):
        metrics_path = run_dir / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path) as f:
                metrics = json.load(f)
            runs.append(
                {
                    "run_id": run_dir.name,
                    "decision": metrics["decision"],
                    "accuracy": metrics["accuracy"],
                    "judge_score": metrics["judge_score"],
                }
            )
    return runs


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    metrics_path = RUNS_DIR / run_id / "metrics.json"
    if not metrics_path.exists():
        raise HTTPException(status_code=404, detail="Run not found")

    with open(metrics_path) as f:
        return json.load(f)

