"""Bounded PRE-LAUNCH follower: at most one fresh event after arming, no backlog."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import time
import uuid

from chatgpt_bridge import ROOT, LONDON, Ledger, submit, target_key, validate

TARGET = "https://chatgpt.com/g/g-p-6aa831a4082881918adcb693c949bba2-trading-test/c/6aa99a20-4c08-83eb-bb61-6f9bce846969"
MAX_FILE = 8 * 1024 * 1024
MAX_LINE = 32768


class NewLines:
    """Read-only source, rejecting rotation/rewrite; exclude initial partial line."""
    def __init__(self, path):
        self.path = Path(path)
        self.identity, self.seen = self.snapshot()
        self.start_offset = len(self.seen)
        self.skip_partial = bool(self.seen and not self.seen.endswith(b'\n'))
        self.pending = b''

    def snapshot(self):
        with self.path.open('rb') as handle:
            info = os.fstat(handle.fileno())
            data = handle.read(MAX_FILE + 1)
        if len(data) > MAX_FILE:
            raise ValueError('Event file exceeds bounded-test 8 MiB limit')
        return (info.st_dev, info.st_ino), data

    def poll(self):
        identity, data = self.snapshot()
        if identity != self.identity or not data.startswith(self.seen):
            raise RuntimeError('Event file replaced, truncated or rewritten; stopped')
        fresh = data[len(self.seen):]
        self.seen = data
        if self.skip_partial:
            boundary = fresh.find(b'\n')
            if boundary < 0:
                return []
            fresh = fresh[boundary + 1:]
            self.skip_partial = False
        chunks = (self.pending + fresh).split(b'\n')
        self.pending = chunks.pop()
        if any(len(line) > MAX_LINE for line in chunks + [self.pending]):
            raise ValueError('Event line exceeds bounded-test limit')
        return chunks


def eligible(event, armed_at, now):
    if not isinstance(event, dict):
        raise ValueError('Event log row must be a JSON object')
    if event.get('record_type') != 'MARKET_EVENT':
        return 'NON_MARKET_EVENT'
    validate(event)
    detected = datetime.fromisoformat(event['watcher_detected_iso'])
    if detected < armed_at:
        return 'PREDATES_ARMING'
    age = (now - detected).total_seconds()
    if age < 0:
        return 'FUTURE_TIMESTAMP'
    if age > 60:
        return 'STALE_EVENT'
    return None


@contextmanager
def follower_lock(ledger):
    path = ledger.lock_path.with_name('follower.lock')
    with path.open('x', encoding='utf-8') as handle:
        handle.write(str(os.getpid()))
        handle.flush()
        os.fsync(handle.fileno())
    try:
        yield
    finally:
        path.unlink()


def follow(events, ledger, seconds=300, sender=submit, clock=None, monotonic=None, sleep=None):
    clock = clock or (lambda: datetime.now(LONDON))
    monotonic = monotonic or time.monotonic
    sleep = sleep or time.sleep
    if not 1 <= seconds <= 900:
        raise ValueError('Bounded test duration must be 1..900 seconds')
    target_key(TARGET)
    session = 'FOLLOW-' + uuid.uuid4().hex
    with follower_lock(ledger):
        outcome = 'ERROR'
        try:
            reader = NewLines(events)
            armed_at = clock()
            deadline = monotonic() + seconds
            ledger.record('FOLLOWER ARMED', session, source=str(Path(events).resolve()),
                          start_offset=reader.start_offset, armed_at=armed_at.isoformat(),
                          target=TARGET, duration_seconds=seconds, maximum_submissions=1,
                          backlog_policy='Skip all bytes present at startup, including partial line')
            print('ARMED: new events only; maximum one message; PRE-LAUNCH', flush=True)
            while monotonic() < deadline:
                for line in reader.poll():
                    if monotonic() >= deadline:
                        break
                    event = json.loads(line)
                    reason = eligible(event, armed_at, clock())
                    if reason:
                        ledger.record('FOLLOWER SKIPPED', session,
                                      source_event_id=event.get('event_id'), reason=reason)
                        continue
                    result = sender(event, TARGET, ledger)
                    if result == 'CHATGPT SUBMITTED':
                        outcome = 'ONE_MESSAGE_SUBMITTED'
                        return outcome
                    # A previously reserved event could have an uncertain send.
                    # Stop this session instead of concealing it by moving on.
                    outcome = 'RESERVED_EVENT_BLOCKED'
                    return outcome
                sleep(min(0.5, max(0, deadline - monotonic())))
            outcome = 'TIMEOUT_NO_SUBMISSION'
            return outcome
        except KeyboardInterrupt:
            outcome = 'INTERRUPTED'
            return outcome
        except Exception as error:
            ledger.record('FOLLOWER ERROR', session, error_type=type(error).__name__, error=str(error))
            raise
        finally:
            ledger.record('FOLLOWER STOPPED', session, outcome=outcome)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=int, default=300)
    args = parser.parse_args()
    config = json.loads((ROOT / 'config/watcher_config.json').read_text(encoding='utf-8-sig'))
    if config.get('test_mode') is not True or config.get('product') != 'BTC-GBP':
        parser.error('Watcher configuration must remain test_mode=true and BTC-GBP')
    ledger = Ledger(ROOT / 'chatgpt_bridge_state/ledger.sqlite3')
    try:
        print(follow(ROOT / 'data/market_events.jsonl', ledger, seconds=args.seconds))
    finally:
        ledger.db.close()


if __name__ == '__main__':
    main()
