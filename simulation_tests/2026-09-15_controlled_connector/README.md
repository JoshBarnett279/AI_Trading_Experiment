# Controlled connector integration test — PASSED

Recorded: 2026-09-15 22:36:14 BST (2026-09-15T22:36:14.766906+01:00). PRE-LAUNCH.

User requested a synthetic test instead of waiting for a real market change.
The test used a separate synthetic JSONL file, appending one event only after
FOLLOWER ARMED appeared in the real ledger. The actual follower, bridge,
dedicated Chrome and exact conversation were used. No mock browser was used.
The real event file and watcher thresholds were not edited. The price watcher
was left running. The waiting 900-second connector PID 25788 was deliberately
stopped for this test; its old lock is preserved as evidence in the state folder.
Its missing normal STOPPED row reflects that deliberate termination, not an
unexplained crash. The intervention was performed before the first test run.

## First run: sent, confirmation failed

20260915-223143-aaf48ae9 preserves the original failed result and timeout.
Read-only inspection found exactly one matching user message, with message ID
f63c12db-6a49-4f44-9fec-e57b153b40ab. ChatGPT appended a Show more control to the
message container, causing exact container-text matching to fail. Reconciliation
was appended separately; the original failure was not rewritten or retried.
The first event's duplicate was blocked without another send. Its precise
submission timestamp is unknown; the later reconciliation time is not substituted.

## Fix and successful fresh run

Message matching now compares collapsible-user-message-content when present,
excluding its controls; ordinary messages retain exact matching. It still
requires a displayed user-message container and exact full content, not a prefix.
22 offline regression tests passed, including two new confirmation tests.

20260915-223501-d982a394 contains the fresh run's actual event, audit and result.
It passed synthetic file append -> follower -> bridge -> ChatGPT submission.
The subsequent duplicate check also passed. This was a new regression test after
resolving the first event's delivery, not a retry of an ambiguous reservation.

Controlled integration is TESTED. Natural-market-triggered delivery remains
UNTESTED. No trading decisions, trades, rule freeze, capital initialization or
official 30-day clock start occurred. All test follower sessions have ended.

To deliberately repeat later: python -B test_connector_live.py. Each invocation
creates a new synthetic event and can send one message; do not rerun after an
uncertain result until that event is reconciled. The harness creates evidence
under this directory and preserves failures as well as successes.
