from pathlib import Path
from datetime import datetime
import shutil
import json
import random
import yaml

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("runs") / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # load config
    config_path = Path("configs/default.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    learning_rate = config["learning_rate"]
    epochs = config["epochs"]

    # copy config into run
    shutil.copy(config_path, run_dir / "config.yaml")

    # fake metric influenced by config (on purpose)
    base = random.uniform(0.6, 0.7)
    accuracy = round(base + epochs * 0.01 - learning_rate, 4)

    metrics = {
        "accuracy": accuracy,
        "epochs": epochs,
        "learning_rate": learning_rate
    }

    with open(run_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(
        f"Run {timestamp} | "
        f"epochs={epochs}, lr={learning_rate}, accuracy={accuracy}"
    )

if __name__ == "__main__":
    main()

