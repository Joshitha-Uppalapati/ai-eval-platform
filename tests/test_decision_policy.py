def decision_from_score(score: float) -> str:
    if score >= 0.8:
        return "PASS"
    if score >= 0.5:
        return "REVIEW"
    return "FAIL"


def test_decision_pass():
    assert decision_from_score(1.0) == "PASS"


def test_decision_review():
    assert decision_from_score(0.6) == "REVIEW"


def test_decision_fail():
    assert decision_from_score(0.2) == "FAIL"

