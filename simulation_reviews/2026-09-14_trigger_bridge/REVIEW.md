# Review: watcher-to-queue simulation

Review created: 2026-09-14 20:52:57 BST (2026-09-14T20:52:57+01:00).
Scope: [archived test and data](../../simulation_tests/2026-09-14_trigger_bridge/README.md).

## Verdict

**Partial infrastructure success. Not ready for the 30-day experiment.**
The watcher's real event branch produced an event from injected data, and the
bridge converted it into the correct fixed message without a duplicate on a
second sequential scan. There is no demonstrated automatic ChatGPT receipt.
No return, profit, trading accuracy or execution-quality conclusion is possible.

| Check | Evidence | Result |
|---|---|---|
| Threshold event | 60,000 to 60,600; +1.0%; 301 simulated seconds | Passed for this upward case |
| Event-to-message mapping | One outbox entry; fixed test message | Passed |
| Sequential restart deduplication | Second collection returned zero; bytes unchanged | Passed |
| Filtering | Unit test rejects non-test events and watcher errors | Passed for covered cases |
| Incomplete writes | Unit test waits for source newline and rejects damaged outbox tail | Passed for covered cases |
| London timestamps | Original offset-aware records; winter GMT/summer BST test | Passed for covered dates |
| Desktop delivery / response | No configured transport or receipt | Not tested |
| Trading simulation / 30-day performance | No execution engine or portfolio test in this run | Not tested |

## Improvements, in priority order

1. **Establish and prove immediate desktop delivery.** Find a supported transport,
   then send one fixed test message and retain the actual app response and receipt
   timestamp. Keep this distinct from queued, launched or submitted states. The
   user chose continued immediate-delivery investigation over scheduled polling.
2. **Add delivery tracking and recovery.** Use append-only attempted, acknowledged,
   failed and uncertain states linked to the event ID. Test app closed, offline,
   timeout and restart cases. Avoid blind retries after ambiguous acceptance.
3. **Prevent concurrent duplicates.** The prototype supports one collector only.
   Two simultaneous collectors can both enqueue the same event. Add a lock or
   transactional claim and test competing processes and crashes.
4. **Improve test provenance.** Future events should explicitly identify synthetic
   input, a test-run ID and simulated clock use instead of retaining a misleading
   Coinbase label. Add corrections or sidecar provenance for historical data;
   do not edit the archived raw evidence.
5. **Expand meaningful coverage.** Test negative moves, exact threshold boundaries,
   cooldown, stale data, unknown products, invalid IDs, malformed JSON, file
   rotation/truncation and DST transitions. Existing tests cover only a subset.
6. **Improve reproducibility.** Parameterize the probe's watcher path, record Python
   and tzdata versions, and save test output and exit codes automatically. Keep
   each run in a new directory with a timestamp and hashes.
7. **Bound polling cost and define replay policy.** The collector rescans the entire
   log and accepts all eligible historical test events. Add a durable cursor or
   explicit start boundary, and define freshness rules before continuous use.

## Audit and data limitations

The files are append-only by application convention, not tamper-proof. Manifest
hashes provide a comparison baseline but do not prevent later alteration. The
live data snapshot is a separate finite capture while the watcher was running;
it is not part of the injected-price test and is not a complete future history.
The raw audit contains its original local evidence path for provenance.

No existing watcher files, rules, portfolio balances or historical logs were
modified for this archive. The experiment clock remains stopped.
