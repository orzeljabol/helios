from fastapi.testclient import TestClient

from helios.main import app


def test_api_post_return_response() -> None:
    client = TestClient(app)
    response = client.post(
        "/inference",
        json={"prompt": "Explain queues.", "deadline_ms": 3000, "priority": 2},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["worker_id"] == "worker-1"
    assert isinstance(data["request_id"], str)
    assert data["request_id"]
    assert data["result"] == "worker-1 processed: Explain queues."
