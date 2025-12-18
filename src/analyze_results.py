import csv
from pathlib import Path
import matplotlib.pyplot as plt

EXPERIMENTS_CSV = Path("experiments.csv")
ANALYSIS_DIR = Path("analysis")
PLOT_PATH = ANALYSIS_DIR / "accuracy_vs_threshold.png"


def main():
    ANALYSIS_DIR.mkdir(exist_ok=True)

    rows = []
    with open(EXPERIMENTS_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("threshold"):
                rows.append({
                    "run_id": row["run_id"],
                    "accuracy": float(row["accuracy"]),
                    "threshold": float(row["threshold"])
                })

    if not rows:
        print("No runs with threshold found.")
        return

    accuracies = [r["accuracy"] for r in rows]
    thresholds = [r["threshold"] for r in rows]

    best = max(rows, key=lambda r: r["accuracy"])
    worst = min(rows, key=lambda r: r["accuracy"])
    avg_accuracy = sum(accuracies) / len(accuracies)

    print("Experiment analysis")
    print("-" * 20)
    print(f"Total analyzed runs: {len(rows)}")
    print(f"Average accuracy: {avg_accuracy:.4f}")
    print(
        f"Best run: {best['run_id']} "
        f"(accuracy={best['accuracy']}, threshold={best['threshold']})"
    )
    print(
        f"Worst run: {worst['run_id']} "
        f"(accuracy={worst['accuracy']}, threshold={worst['threshold']})"
    )

    # -------- Plot --------
    plt.figure(figsize=(6, 4))

    plt.scatter(
        thresholds,
        accuracies,
        s=80,
        alpha=0.8
    )

    best_accuracy = max(accuracies)
    plt.axhline(
        y=best_accuracy,
        linestyle="--",
        linewidth=1,
        label=f"Best accuracy = {best_accuracy:.2f}"
    )

    plt.xlabel("Threshold")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Threshold")

    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()

    plt.savefig(PLOT_PATH)
    plt.close()

    print(f"\nSaved plot to {PLOT_PATH}")


if __name__ == "__main__":
    main()

