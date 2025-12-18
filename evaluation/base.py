from typing import Dict


class BaseJudge:
    name = "base"
    version = "base-v0"

    def evaluate(self, prediction: str, reference: str) -> Dict:
        raise NotImplementedError("Judge must implement evaluate()")

