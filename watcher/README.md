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
python -m pip install -r requirements.txt
python watcher/market_watcher.py
```

Python 3.9+ is recommended because the watcher uses the standard-library `zoneinfo` module.

## Windows timezone dependency

**Updated: 2026-09-15 05:29:22 BST**

Windows testing exposed a missing IANA timezone-data issue. It was resolved with:

```text
python -m pip install tzdata
```

The dependency is now listed in the repository `requirements.txt`. On systems with their own IANA timezone database it may be redundant, but keeping it explicit makes `Europe/London` timestamping portable on Windows.

## Current development configuration

The initial test configuration is stored in `config/watcher_config.json`.

**Verified/recorded: 2026-09-15 05:29:22 BST**

- product: `BTC-GBP`
- polling: 15 seconds
- rolling lookback: 300 seconds / 5 minutes
- trigger: ±0.5% over the lookback

The ±0.5%/5-minute trigger is **TEST ONLY**. It is not a live trading rule and is not frozen. Final filtering is expected to be tuned/replaced with smarter multi-window triggers that may incorporate volatility, volume, news and portfolio context.

## Test status

**Recorded: 2026-09-15 05:29:22 BST**

- **IMPLEMENTED + TESTED:** real Coinbase BTC-GBP collection on Windows.
- **IMPLEMENTED + TESTED:** 15-second polling and rolling 5-minute movement calculation.
- **TESTED:** synthetic threshold event → local deduplicated message queue bridge.
- **UNCONFIRMED:** automatic delivery/receipt by ChatGPT.
- **UNCONFIRMED:** cause of one unexpected watcher/CMD closure. Event Viewer showed no relevant Application crash; Ctrl+C stopped Python without closing CMD; accidental manual closure is possible but unproven.
- **PLANNED before launch:** persistent crash/error logs, automatic recovery, timestamped component heartbeats and failure alerts.

## Runtime files

The watcher creates these files automatically when run:

```text
data/market_observations.jsonl
data/market_events.jsonl
```

Both are append-only runtime logs. Test records contain `"test_mode": true` so they cannot be confused with live-experiment records.

## Efficiency boundary

**Design recorded: 2026-09-15 05:29:22 BST**

Routine monitoring/logging/filtering must remain local and consume no AI tokens. Events should be filtered and deduplicated locally, then sent as compact event packets only when meaningful AI analysis is warranted. If AI access is unavailable, fail safely and log it rather than attempting to bypass usage limits.

## Next development milestone

**Updated: 2026-09-15 05:29:22 BST**

Prove automatic event → ChatGPT triggering and receipt. This remains PRE-LAUNCH infrastructure work. No trading authority is attached to the watcher and the official 30-day clock remains **NOT STARTED**.
