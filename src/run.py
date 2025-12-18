import sys
from pathlib import Path
from datetime import datetime
import shutil
import json
import yaml


def compute_accuracy(y_true, y_pred):
    correct = 0
    for t, p in zip(y_true, y_pred):
        if t == p:
            correct += 1
    return correct / len(y_true)


def main():
    # read config path from command line (optional)
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        config_path = Path("configs/default.yaml")

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # load config
    with open(config_path) as f:
        config = yaml.safe_load(f)

    learning_rate = config["learning_rate"]
    epochs = config["epochs"]

    # copy config into run
    shutil.copy(config_path, run_dir / "config.yaml")

    # fake data, real evaluation logic
    y_true = [1, 0, 1, 1, 0, 1, 0, 0]
    y_pred = [1, 1, 1, 0, 0, 1, 0, 1]

    accuracy = round(compute_accuracy(y_true, y_pred), 4)

    metrics = {
        "accuracy": accuracy,
        "epochs": epochs,
        "learning_rate": learning_rate
    }

    with open(run_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(
        f"Run {timestamp} | "
        f"config={config_path.name}, "
        f"epochs={epochs}, lr={learning_rate}, accuracy={accuracy}"
    )


if __name__ == "__main__":
    main()

