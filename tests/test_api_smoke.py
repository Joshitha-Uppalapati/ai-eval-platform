from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_run_endpoint():
    response = client.post("/run")
    assert response.status_code == 200

    data = response.json()
    assert "run_id" in data
    assert "decision" in data
    assert "accuracy" in data
    assert "judge_score" in data
