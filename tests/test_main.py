import asyncio

from helios.events import EventLog, EventType
from helios.main import process_inference
from helios.models import InferenceRequest
from helios.policy import SingleWorkerPolicy
from helios.worker import MockWorker


def test_process_inference_returns_result_and_records_events() -> None:
    worker = MockWorker(
        worker_id="worker-1",
        base_latency_ms=1,
        capacity=1,
        healthy=True,
    )

    policy = SingleWorkerPolicy(worker)
    event_log = EventLog()

    request = InferenceRequest(
        prompt="Explain queues.",
        deadline_ms=3000,
        priority=2,
    )

    result = asyncio.run(
        process_inference(
            request=request,
            request_id="request-1",
            policy=policy,
            event_log=event_log,
        )
    )

    events = event_log.get_events()

    assert result == "worker-1 processed: Explain queues."
    assert len(events) == 4
    assert [event.event_type for event in events] == [
        EventType.REQUEST_RECEIVED,
        EventType.WORKER_SELECTED,
        EventType.EXECUTION_STARTED,
        EventType.EXECUTION_COMPLETED,
    ]
