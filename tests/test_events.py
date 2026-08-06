from datetime import UTC, datetime

from helios.events import Event, EventLog, EventType


def test_event_log_records_event() -> None:
    event_log = EventLog()

    event = Event(
        event_type=EventType.REQUEST_RECEIVED,
        timestamp=datetime.now(UTC),
        request_id="request-1",
        worker_id=None,
    )

    event_log.record(event)

    assert event_log.get_events() == [event]
