from pathlib import Path
import json
import csv

FIELDS = ["run_id", "accuracy", "epochs", "learning_rate"]

def main():
    runs_dir = Path("runs")
    output_path = Path("experiments.csv")

    rows = []

    for run_dir in sorted(runs_dir.iterdir()):
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
        }
        rows.append(row)

    if not rows:
        print("No runs with metrics found.")
        return

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} runs to {output_path}")

if __name__ == "__main__":
    main()
