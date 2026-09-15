"""Explicit controlled PRE-LAUNCH test: sends one synthetic event via real Chrome."""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import threading
import time
import uuid
from datetime import datetime

from chatgpt_bridge import ROOT, LONDON, Browser, Ledger, stamp, submit
from watch_chatgpt_bridge import TARGET, follow


def append(path, value):
    with path.open('ab') as out:
        out.write((json.dumps(value) + '\n').encode())
        out.flush()
        os.fsync(out.fileno())


def main():
    run_id = datetime.now(LONDON).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
    run = ROOT / 'simulation_tests/2026-09-15_controlled_connector' / run_id
    run.mkdir(parents=True, exist_ok=False)
    events = run / 'synthetic_events.jsonl'
    events.touch()
    ledger_path = ROOT / 'chatgpt_bridge_state/ledger.sqlite3'
    ledger = Ledger(ledger_path)
    event_id = 'SYNTHETIC-CONNECTOR-' + uuid.uuid4().hex
    immutable_paths = ['watcher/market_watcher.py', 'config/watcher_config.json', 'RULES.md']
    before = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in immutable_paths}
    errors, generated = [], []
    stop = threading.Event()
    result = 'NOT_COMPLETED'
    producer = None
    start_seq = ledger.db.execute('SELECT coalesce(max(seq),0) FROM audit').fetchone()[0]
    try:
        if (ROOT/'chatgpt_bridge_state/follower.lock').exists():
            raise RuntimeError('Another follower is active or requires lock inspection')
        browser = Browser()
        try:
            browser.prepare(TARGET)
        finally:
            browser.close()
        ledger.record('CONTROLLED TEST STARTED', event_id, synthetic=True, source=str(events),
                      reason='User requested a controlled test instead of waiting for market movement')

        def produce():
            db = sqlite3.connect(ledger_path.as_uri() + '?mode=ro', uri=True)
            try:
                deadline = time.monotonic() + 15
                while not stop.is_set() and time.monotonic() < deadline:
                    rows = [json.loads(r[0]) for r in db.execute('SELECT record FROM audit WHERE seq>?', (start_seq,))]
                    if any(r['record_type'] == 'FOLLOWER ARMED' and r.get('source') == str(events.resolve()) for r in rows):
                        now = datetime.now(LONDON)
                        value = dict(record_type='MARKET_EVENT', event_id=event_id, product='BTC-GBP',
                                     test_mode=True, synthetic=True, watcher_detected_iso=now.isoformat(),
                                     source='Controlled synthetic connector test; no market detection',
                                     reason='PRE-LAUNCH synthetic delivery test. Acknowledge only; no trading action.')
                        append(events, value)
                        generated.append(value)
                        print('SYNTHETIC EVENT APPENDED AFTER ARMING', flush=True)
                        return
                    stop.wait(0.05)
                if not stop.is_set():
                    raise TimeoutError('Follower did not arm within 15 seconds')
            except Exception as error:
                errors.append(repr(error))
            finally:
                db.close()

        producer = threading.Thread(target=produce, daemon=True)
        producer.start()
        result = follow(events, ledger, seconds=30)
        stop.set()
        producer.join(timeout=2)
        if errors:
            raise RuntimeError('; '.join(errors))
        if result != 'ONE_MESSAGE_SUBMITTED' or len(generated) != 1:
            raise RuntimeError('Controlled test did not submit exactly one generated event: ' + result)
        duplicate = submit(generated[0], TARGET, ledger)
        if not duplicate.startswith('DUPLICATE BLOCKED'):
            raise RuntimeError('Duplicate check failed')
        result = 'PASSED_SUBMISSION_AND_DUPLICATE_BLOCK'
        ledger.record('CONTROLLED TEST PASSED', event_id, synthetic=True,
                      duplicate_result=duplicate, natural_market_delivery_tested=False)
        print(result, flush=True)
    except Exception as error:
        ledger.record('CONTROLLED TEST FAILED', event_id, error_type=type(error).__name__, error=str(error))
        result = 'FAILED'
        raise
    finally:
        stop.set()
        if producer:
            producer.join(timeout=2)
        rows = [json.loads(r[0]) for r in ledger.db.execute('SELECT record FROM audit WHERE seq>? ORDER BY seq', (start_seq,))]
        for r in rows:
            append(run/'audit.jsonl', r)
        preserved = all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == digest for p,digest in before.items())
        summary = dict(**stamp(), phase='PRE-LAUNCH', result=result, event_id=event_id,
                       source_event_file=str(events), synthetic=True, source_code_config_rules_preserved=preserved,
                       before_sha256=before, natural_market_delivery_tested=False,
                       clock_started=False, rules_frozen=False, trades_executed=False)
        (run/'result.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
        ledger.db.close()
        print('Evidence: ' + str(run), flush=True)


if __name__ == '__main__':
    main()
