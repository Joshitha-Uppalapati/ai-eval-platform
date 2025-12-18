import csv
from pathlib import Path
import matplotlib.pyplot as plt

CSV_PATH = Path("experiments.csv")
OUTPUT_DIR = Path("analysis")
PLOT_PATH = OUTPUT_DIR / "accuracy_vs_threshold.png"


def main():
    rows = []

    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip rows without threshold
            if not row.get("threshold"):
                continue

            rows.append({
                "run_id": row["run_id"],
                "accuracy": float(row["accuracy"]),
                "threshold": float(row["threshold"]),
            })

    if not rows:
        print("No runs with threshold found.")
        return

    
    accuracies = [r["accuracy"] for r in rows]
    best = max(rows, key=lambda r: r["accuracy"])
    worst = min(rows, key=lambda r: r["accuracy"])
    avg_accuracy = sum(accuracies) / len(accuracies)

    print("Experiment analysis")
    print("-" * 20)
    print(f"Total analyzed runs: {len(rows)}")
    print(f"Average accuracy: {avg_accuracy:.4f}")
    print(f"Best run: {best['run_id']} (accuracy={best['accuracy']}, threshold={best['threshold']})")
    print(f"Worst run: {worst['run_id']} (accuracy={worst['accuracy']}, threshold={worst['threshold']})")

    thresholds = [r["threshold"] for r in rows]
    accuracies = [r["accuracy"] for r in rows]

    plt.figure()
    plt.scatter(thresholds, accuracies)
    plt.xlabel("Threshold")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Threshold")
    plt.savefig(PLOT_PATH)
    plt.close()

    print(f"\nSaved plot to {PLOT_PATH}")


if __name__ == "__main__":
    main()

