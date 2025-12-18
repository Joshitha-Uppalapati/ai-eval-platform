from pathlib import Path
from datetime import datetime
import shutil
import json
import yaml
import csv
import sys


def main():
    # choose config
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        config_path = Path("configs/default.yaml")

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    # setup run directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # load config
    with open(config_path) as f:
        config = yaml.safe_load(f)

    epochs = config["epochs"]
    learning_rate = config["learning_rate"]
    threshold = config.get("threshold", 0.5)

    # copy config into run
    shutil.copy(config_path, run_dir / "config.yaml")

    # load dataset
    data_path = Path("data/dataset.csv")
    correct = 0
    total = 0

    with open(data_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row["x"])
            label = int(row["label"])

            prediction = 1 if x > threshold else 0
            if prediction == label:
                correct += 1
            total += 1

    accuracy = round(correct / total, 4)

    metrics = {
        "accuracy": accuracy,
        "epochs": epochs,
        "learning_rate": learning_rate,
        "threshold": threshold
    }

    with open(run_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(
        f"Run {timestamp} | "
        f"config={config_path.name}, "
        f"threshold={threshold}, "
        f"accuracy={accuracy}"
    )


if __name__ == "__main__":
    main()

