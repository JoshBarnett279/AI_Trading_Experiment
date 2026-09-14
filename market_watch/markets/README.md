# Individual Market Logs

Created: 2026-09-14 19:40:02 BST

This directory will contain one audit file per watched market or instrument.

Each file should record:

- market/asset identifier
- venue/exchange where relevant
- monitoring start timestamp
- monitoring end timestamp if removed
- data sources
- watcher configuration
- significant detected events
- AI agents/models invoked for related tasks
- links/references to decisions and simulated trades
- failures, stale-data periods, or monitoring interruptions

## Naming Convention

Use a stable, filesystem-safe identifier, for example:

```text
BTC-USD.md
NVDA.md
EUR-USD.md
SPY.md
```

If two instruments could share the same symbol, include the venue or another disambiguator in the filename.

No individual market files exist yet because live monitoring has not started.
