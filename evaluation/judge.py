from typing import Dict
from evaluation.base import BaseJudge


class MockJudge(BaseJudge):
    name = "mock"
    version = "mock-v1"

    def evaluate(self, prediction: str, reference: str) -> Dict:
        if prediction == reference:
            return {
                "score": 1.0,
                "verdict": "pass",
                "reason": "Prediction exactly matches reference.",
                "judge_version": self.version,
            }

        if prediction in reference or reference in prediction:
            return {
                "score": 0.5,
                "verdict": "partial",
                "reason": "Prediction partially matches reference.",
                "judge_version": self.version,
            }

        return {
            "score": 0.0,
            "verdict": "fail",
            "reason": "Prediction does not match reference.",
            "judge_version": self.version,
        }


def get_judge(judge_type: str = "mock") -> BaseJudge:
    if judge_type == "mock":
        return MockJudge()

    raise ValueError(f"Unknown judge type: {judge_type}")

