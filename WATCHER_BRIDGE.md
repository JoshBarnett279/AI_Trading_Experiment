# Bounded watcher-to-ChatGPT connector — PRE-LAUNCH

`watch_chatgpt_bridge.py` connects newly appended watcher events to the existing
tested `chatgpt_bridge.py`. It does not change the watcher, its thresholds,
historical records or frozen status. Messages request acknowledgment only.

## First live test, one small step at a time

1. In CMD at the repository root, start the original watcher:
   `python watcher\market_watcher.py`.
   Leave this window open. It takes at least five minutes to rebuild price
   history after a restart. No Python watcher process was present at the
   implementation check; last observation was 2026-09-15 02:01:42 BST. The
   precise stopping time and cause are UNCONFIRMED.
2. Keep dedicated Chrome open to Trading Experiment Live Bridge, with an empty
   composer. In a second CMD window at the repository root, run
   `python watch_chatgpt_bridge.py --seconds 900`.
3. This arms a maximum 15-minute session and sends at most one fresh test event.
   It prints ONE_MESSAGE_SUBMITTED, RESERVED_EVENT_BLOCKED, INTERRUPTED or
   TIMEOUT_NO_SUBMISSION, then exits. The default duration is five minutes.
   A send started before the deadline can finish after it, including Selenium
   attachment and its 30-second confirmation wait. The duration bounds event
   polling, not every external driver operation.
4. Preserve the console result and review `python chatgpt_bridge.py --export-audit`.
   A timeout means no qualifying event was submitted; it does not prove end-to-end
   delivery. Do not inject synthetic rows into the real watcher file to force it.

The target URL is fixed to the dedicated conversation verified in the prior
isolated test. No background service or automatic restart is installed.

## New events only

At every start, the connector records the current byte length and begins after
it. All earlier records are excluded, including an incomplete final record
whose remaining bytes arrive later. New incomplete records wait for a newline.
Records must be MARKET_EVENT, BTC-GBP, test_mode=true, and pass the existing
bridge schema checks. Detection time must be at/after arming, not in the future,
and at most 60 seconds old. These are test transport limits, not trading rules.
The watcher's second-resolution timestamps can exclude a boundary event from
the same second as arming; this deliberately favors avoiding older events.

Every restart establishes a new boundary: events during downtime are skipped,
not replayed. There is no lossless delivery guarantee or persistent backlog.
All original source records remain in place for audit. Before unattended use,
design outage handling, explicit reconciliation, health monitoring and budgets.

The read-only follower rejects deletion, replacement, truncation or rewriting
of the source file. This bounded prototype compares the full observed prefix
on each half-second poll and stops above 8 MiB. It is intended for a small event
log, not the larger observations file. New rows over 32 KiB and malformed JSON
stop the session. Non-market records are skipped with an audit entry.

## Duplicate protection and failures

The same authoritative SQLite ledger and bridge reservations protect sends.
An exclusive follower.lock prevents concurrent follower sessions. The bridge's
separate lock prevents simultaneous browser sends from the manual and follower
commands. An existing reservation or any send error stops the follower; it
does not silently advance to another event. Never delete reservations to retry.
After a crash, inspect the source, conversation and audit and confirm all related
processes stopped before removing a stale lock only. Preserve the database.

FOLLOWER ARMED / SKIPPED / ERROR / STOPPED records use Europe/London timestamps
with BST/GMT and ISO offsets. BRIDGE RECEIVED and CHATGPT SUBMITTED retain their
existing meanings. Visible submission does not establish AI processing time.

## Validation boundary

Twenty offline tests passed: ten existing bridge tests and ten connector tests.
Connector coverage includes old-record exclusion, restart exclusion, partial
lines at startup and after startup, rewrite/truncation/replacement detection,
freshness/test-mode filtering, one-message cap, uncertain-send stop, timeout,
source preservation and concurrent-follower exclusion. Browser sends are mocked
in these tests. The original Selenium bridge was separately live-tested earlier.
This new watcher-to-browser route awaits a naturally generated event test.

Run tests with `python -B -m unittest discover -p "test*bridge.py" -v`.
No trades, rule freeze, official opening balance or 30-day start are performed.
