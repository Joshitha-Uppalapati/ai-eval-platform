from pathlib import Path
from datetime import datetime
import shutil
import json
import yaml
import csv
import sys

from evaluation.judge import get_judge
from evaluation.decision import decide_run


def main():
    # Choose config
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        config_path = Path("configs/default.yaml")

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    # Setup run directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # Load config
    with open(config_path) as f:
        config = yaml.safe_load(f)

    epochs = config["epochs"]
    learning_rate = config["learning_rate"]
    threshold = config.get("threshold", 0.5)

    judge_type = config.get("judge", {}).get("type", "mock")
    judge = get_judge(judge_type)

    # Copy config into run directory
    shutil.copy(config_path, run_dir / "config.yaml")

    # Load Golden Dataset
    data_path = Path("data/dataset.csv")
    if not data_path.exists():
        raise FileNotFoundError("Golden dataset not found: data/dataset.csv")

    correct = 0
    total = 0

    judge_scores = []
    judge_verdicts = {
        "pass": 0,
        "partial": 0,
        "fail": 0,
    }

    # Run evaluation
    with open(data_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row["x"])
            label = int(row["label"])

            prediction = 1 if x > threshold else 0

            # Accuracy metric
            if prediction == label:
                correct += 1
            total += 1

            # Judge evaluation
            judge_result = judge.evaluate(
                prediction=str(prediction),
                reference=str(label),
            )

            judge_scores.append(judge_result["score"])
            judge_verdicts[judge_result["verdict"]] += 1

    # Aggregate metrics
    accuracy = round(correct / total, 4)
    avg_judge_score = round(sum(judge_scores) / len(judge_scores), 4)

    metrics = {
        "accuracy": accuracy,
        "epochs": epochs,
        "learning_rate": learning_rate,
        "threshold": threshold,
        "judge_score": avg_judge_score,
        "judge_breakdown": judge_verdicts,
        "judge_version": judge.version,
    }

    # Decision policy (Stage 11)
    decision_payload = decide_run(metrics)
    metrics.update(decision_payload)

    # Save metrics
    with open(run_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Console output
    print(
        f"Run {timestamp} | "
        f"config={config_path.name}, "
        f"threshold={threshold}, "
        f"accuracy={accuracy}, "
        f"judge_score={avg_judge_score}, "
        f"decision={metrics['decision']}"
    )

    # CI enforcement (Stage 12)
    if metrics["decision"] == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
