from pathlib import Path
import json
import csv

RUNS_DIR = Path("runs")
OUTPUT_CSV = Path("experiments.csv")


def main():
    rows = []

    for run_dir in sorted(RUNS_DIR.iterdir()):
        metrics_path = run_dir / "metrics.json"
        if not metrics_path.exists():
            continue

        with open(metrics_path) as f:
            metrics = json.load(f)

        row = {
            "run_id": run_dir.name,
            "accuracy": metrics.get("accuracy"),
            "epochs": metrics.get("epochs"),
            "learning_rate": metrics.get("learning_rate"),
            "threshold": metrics.get("threshold"),
            "dataset": "dataset.csv",
        }

        rows.append(row)

    if not rows:
        print("No runs found.")
        return

    fieldnames = [
        "run_id",
        "accuracy",
        "epochs",
        "learning_rate",
        "threshold",
        "dataset",
    ]

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} runs to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

