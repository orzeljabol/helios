from fastapi.testclient import TestClient

from helios.main import app, event_log


def test_api_post_return_response() -> None:
    event_log.clear()
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
    assert len(event_log.get_events()) == 4


def test_api_rejects_invalid_request() -> None:
    event_log.clear()
    client = TestClient(app)
    response = client.post(
        "/inference",
        json={"prompt": "", "deadline_ms": 0, "priority": -1},
    )
    data = response.json()
    assert response.status_code == 422
    assert data["detail"]
    assert event_log.get_events() == []
