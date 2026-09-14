# Market Watcher

Created: 2026-09-14 20:20:54 BST  
Status: PRE-LAUNCH TESTING ONLY

The first watcher prototype monitors **BTC-GBP** using Coinbase's public spot-price endpoint.

It currently performs only infrastructure work:

- fetches BTC-GBP spot price
- timestamps observations in `Europe/London`
- appends observations to `data/market_observations.jsonl`
- compares the current price with a configurable historical lookback
- creates a unique event when the configured move threshold is reached
- applies a cooldown to reduce duplicate alerts
- records data-fetch failures rather than inventing prices

It does **not** place trades, make discretionary trading decisions, invoke the live experiment, or start the 30-day clock.

## Run

From the repository root:

```text
python watcher/market_watcher.py
```

Python 3.9+ is recommended because the watcher uses the standard-library `zoneinfo` module. No third-party Python packages are required for this first prototype.

## Current development configuration

The initial test configuration is stored in `config/watcher_config.json`.

The initial settings intentionally use development thresholds and are not live trading rules. They may be altered during pre-launch testing. Any eventual live configuration will be reviewed and frozen before the official experiment begins.

## Runtime files

The watcher creates these files automatically when run:

```text
data/market_observations.jsonl
data/market_events.jsonl
```

Both are append-only runtime logs. Test records contain `"test_mode": true` so they cannot be confused with live-experiment records.

## Next development milestone

After the watcher is proven to collect and timestamp live data reliably, the next milestone is to prove that a generated event can automatically invoke an AI review without creating a hindsight gap.
