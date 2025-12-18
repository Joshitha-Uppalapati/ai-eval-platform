from __future__ import annotations

import csv
import json
from pathlib import Path


EXPERIMENTS_CSV = Path("experiments.csv")
OUTPUT_JSON = Path("analysis") / "best_experiment.json"


def parse_float(value: str) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_rows(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing file: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def select_best(rows: list[dict]) -> dict:
    valid = []
    for r in rows:
        acc = parse_float(r.get("accuracy", ""))
        thr = parse_float(r.get("threshold", ""))
        if acc is None or thr is None:
            continue
        r["_accuracy"] = acc
        r["_threshold"] = thr
        valid.append(r)

    if not valid:
        raise ValueError("No comparable runs found (need rows with accuracy + threshold).")

    valid.sort(key=lambda r: (-r["_accuracy"], r.get("run_id", "")))
    best = valid[0]

    return {
        "run_id": best.get("run_id"),
        "accuracy": best["_accuracy"],
        "threshold": best["_threshold"],
        "epochs": parse_float(best.get("epochs", "")),
        "learning_rate": parse_float(best.get("learning_rate", "")),
        "dataset": best.get("dataset"),
        "reason": "highest accuracy (tie-break: smallest run_id)",
    }


def main() -> None:
    rows = load_rows(EXPERIMENTS_CSV)
    best = select_best(rows)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(best, indent=2), encoding="utf-8")

    print("Best experiment selected")
    print(f"run_id: {best['run_id']}")
    print(f"accuracy: {best['accuracy']}")
    print(f"threshold: {best['threshold']}")
    if best.get("dataset"):
        print(f"dataset: {best['dataset']}")
    print(f"\nSaved: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()

