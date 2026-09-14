"""Pre-launch event-to-outbox adapter. Delivery is a separate, unconfigured step."""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

MESSAGE = "AUTOMATED TEST 001"
LONDON = ZoneInfo("Europe/London")


def records(path):
    if not path.exists():
        return []
    result = []
    with path.open("rb") as stream:
        for line in stream:
            if not line.endswith(b"\n"):
                break  # The watcher may still be writing this record.
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("Expected a JSON object")
            result.append(value)
    return result


def append(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as stream:
        stream.write((json.dumps(record, ensure_ascii=False) + "\n").encode())
        stream.flush()
        os.fsync(stream.fileno())


def collect(events, outbox):
    """Single-consumer prototype; fail closed on a damaged outbox."""
    if events.resolve() == outbox.resolve():
        raise ValueError("Outbox must be separate from watcher events")
    if outbox.exists() and outbox.stat().st_size:
        with outbox.open("rb") as stream:
            stream.seek(-1, 2)
            if stream.read(1) != b"\n":
                raise ValueError("Incomplete outbox; preserve it for inspection")
    existing = {r["event_id"] for r in records(outbox)}
    count = 0
    for event in records(events):
        if (event.get("record_type") != "MARKET_EVENT"
                or event.get("test_mode") is not True
                or event.get("product") != "BTC-GBP"):
            continue
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("Test event has no valid event_id")
        if event_id in existing:
            continue
        now = datetime.now(LONDON)
        append(outbox, {
            "record_type": "BRIDGE_TEST_QUEUED",
            "event_id": event_id,
            "source_event": event,
            "message": MESSAGE,
            "timestamp_london": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "timestamp_iso": now.isoformat(timespec="seconds"),
            "timezone": "Europe/London",
            "test_mode": True,
            "status": "QUEUED_NOT_DELIVERED",
        })
        existing.add(event_id)
        count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--outbox", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps({"queued": collect(args.events, args.outbox), "delivered": False}))
