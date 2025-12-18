from evaluation.judge import MockJudge


def test_judge_pass():
    judge = MockJudge()
    result = judge.evaluate("yes", "yes")
    assert result["score"] == 1.0
    assert result["verdict"] == "pass"


def test_judge_partial():
    judge = MockJudge()
    result = judge.evaluate("yes", "maybe yes")
    assert result["score"] == 0.5
    assert result["verdict"] == "partial"


def test_judge_fail():
    judge = MockJudge()
    result = judge.evaluate("no", "yes")
    assert result["score"] == 0.0
    assert result["verdict"] == "fail"
