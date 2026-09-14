# Pre-launch simulation test: watcher to message queue

Archived: 2026-09-14 20:52:57 BST (2026-09-14T20:52:57+01:00).

Result: **local event-to-queue test passed; desktop delivery not connected**.
This is an infrastructure simulation, not a trading-performance simulation.
The 30-day experiment has not started. No trades or AI trading decisions occurred.

## What is included

- `original_bridge/`: exact bridge code, tests, original notes and all saved test evidence.
- `watcher_snapshot/`: exact watcher and configuration used by the isolated probe.
- `live_watcher_snapshot/`: separate snapshot of all complete local watcher data records available at archival time. These are real observations, not inputs to the synthetic test.
- `manifest.json`: file hashes, snapshot time, data counts and provenance.
- [Results and improvements](../../simulation_reviews/2026-09-14_trigger_bridge/REVIEW.md).

## Synthetic test

Run: `20260914-204814-969831`; event: `EVT-20260914-204814-147D783A`.
Two injected BTC-GBP prices, GBP 60,000 and GBP 60,600, are separated by
301 simulated seconds. The watcher computes +1.0%, exceeding the configured
0.5% threshold over a 300-second lookback, and produces one event.
The adapter queues one `AUTOMATED TEST 001` message. A second collection
queues zero additional messages and preserves the existing outbox bytes.

The original JSONL source label says Coinbase because the watcher emits it;
**these two test prices were synthetic and no Coinbase call occurred in the probe**.
Original observations and timestamps are retained without rewriting history.
The probe backdated its first simulated observation by 301 seconds; it did not
actually wait five minutes. This test cannot establish real delivery latency.

## Validation recorded in the setup session

Three unit tests passed: event filtering/restart deduplication/source preservation;
partial event writes and incomplete outbox rejection; GMT/BST date handling.
The first sandboxed attempt had temporary-directory permission errors; the
subsequent explicitly elevated run passed all three tests. No original test-run
transcript file was saved, so this statement records the observed tool output.
The isolated watcher probe passed and its original JSONL evidence is included.

## Reproduction limits

Python 3.12 was used; install `tzdata` where the OS has no IANA timezone data.
From `original_bridge`, run `python -B -m unittest discover -s . -v`.
The archived probe preserves its original absolute local watcher path and is
not portable unchanged. To rerun elsewhere, adapt a new copy to the archived
watcher snapshot and write a new evidence directory; never overwrite this run.
Run only one collector at a time. The adapter is a one-shot collector with no
desktop transport or installed background process.
