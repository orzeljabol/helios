from helios.policy import SingleWorkerPolicy
from helios.worker import MockWorker


def test_select_worker_returns_configured_worker() -> None:
    worker = MockWorker(
        worker_id="worker-1", base_latency_ms=5, capacity=1, healthy=True
    )

    policy = SingleWorkerPolicy(worker)

    selected = policy.select_worker()

    assert selected is worker
