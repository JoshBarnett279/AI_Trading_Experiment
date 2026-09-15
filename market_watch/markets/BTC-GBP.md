# BTC-GBP Watch Record

Created: 2026-09-14 20:20:54 BST  
Status: PRE-LAUNCH TESTING

## Instrument

- Market ID: `BTC-GBP`
- Asset: Bitcoin
- Quote currency: GBP
- Asset class: Cryptocurrency
- Initial data source: Coinbase public spot-price endpoint

## Monitoring History

**2026-09-14 20:20:54 BST — Added for first watcher prototype.**

Purpose: verify live data retrieval, `Europe/London` timestamping, append-only observation logging, price-move detection, unique event creation and duplicate-event cooldown behaviour.

This monitoring is explicitly test-only and does not start the official 30-day experiment.

**2026-09-15 05:29:22 BST — Windows watcher test status recorded.**

**IMPLEMENTED + TESTED:** the watcher successfully collected real Coinbase BTC-GBP spot data on Windows at approximately 15-second intervals and maintained the configured rolling 300-second / 5-minute movement calculation. Archived observations from the live test remain separate from synthetic bridge inputs.

**IMPLEMENTED, TEST ONLY:** the current ±0.5% over 5 minutes event threshold is an engineering trigger only. It is not frozen strategy logic. Final tuning may use multiple windows plus volatility, volume, news significance and portfolio context before deciding an event deserves AI review.

**UNCONFIRMED:** one watcher/CMD session unexpectedly closed. Windows Event Viewer showed no relevant Application crash, and a Ctrl+C test stopped Python without closing CMD. Accidental manual closure is possible but not established. Persistent crash/error logging and automatic recovery are required before launch.

## Initial Test Parameters

The current development configuration is stored in `config/watcher_config.json`. These thresholds are temporary engineering settings, not frozen trading strategy parameters.

## Trading Status

No trading authority is attached to this watcher. The watcher may detect and log an event, but it cannot execute BUY, SELL or HOLD decisions.

**Checkpoint: 2026-09-15 05:29:22 BST — PRE-LAUNCH; official 30-day clock NOT STARTED.**
