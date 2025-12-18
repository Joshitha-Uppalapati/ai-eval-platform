from pathlib import Path
import json

def main():
    runs_dir = Path("runs")

    print(f"{'RUN ID':<20} ACCURACY")
    print("-" * 32)

    for run_dir in sorted(runs_dir.iterdir()):
        metrics_path = run_dir / "metrics.json"
        if not metrics_path.exists():
            continue

        with open(metrics_path) as f:
            metrics = json.load(f)

        accuracy = metrics.get("accuracy", "N/A")
        print(f"{run_dir.name:<20} {accuracy}")

if __name__ == "__main__":
    main()

