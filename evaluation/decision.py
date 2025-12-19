def decide_run(metrics: dict) -> dict:
    accuracy = metrics.get("accuracy", 0.0)
    judge_score = metrics.get("judge_score", 0.0)

    if judge_score >= 0.8 and accuracy >= 0.8:
        decision = "PASS"
        reason = "High judge score and accuracy meet acceptance thresholds."

    elif judge_score < 0.4 or accuracy < 0.5:
        decision = "FAIL"
        reason = "Judge score or accuracy below minimum threshold."

    else:
        decision = "REVIEW"
        reason = "Mixed signals between metrics and judge score."

    return {
        "decision": decision,
        "decision_reason": reason,
        "policy_version": "v1",
    }

