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

## Initial Test Parameters

The current development configuration is stored in `config/watcher_config.json`. These thresholds are temporary engineering settings, not frozen trading strategy parameters.

## Trading Status

No trading authority is attached to this watcher. The watcher may detect and log an event, but it cannot execute BUY, SELL or HOLD decisions.
