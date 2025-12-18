import json
from typing import Dict


def mock_judge(
    prediction: str,
    reference: str
) -> Dict:

    if prediction.strip() == reference.strip():
        verdict = "pass"
        score = 1.0
        reason = "Prediction exactly matches reference."
    elif prediction.strip() in reference.strip() or reference.strip() in prediction.strip():
        verdict = "partial"
        score = 0.5
        reason = "Prediction partially matches reference."
    else:
        verdict = "fail"
        score = 0.0
        reason = "Prediction does not match reference."

    return {
        "score": score,
        "verdict": verdict,
        "reason": reason,
        "judge_version": "mock-v1"
    }


def save_judgment(judgment: Dict, output_path: str) -> None:
    with open(output_path, "w") as f:
        json.dump(judgment, f, indent=2)

