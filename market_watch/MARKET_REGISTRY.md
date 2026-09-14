# Market Registry

Created: 2026-09-14 19:40:02 BST
Last updated: 2026-09-14 20:20:54 BST

This registry lists every market, asset, or instrument watched by the experiment.

| Market ID | Asset / Instrument | Asset Class | Venue / Exchange | Data Source | Status | Added | Removed | Notes |
|---|---|---|---|---|---|---|---|---|
| BTC-GBP | Bitcoin / British Pound | Cryptocurrency | Coinbase spot reference | Coinbase public spot endpoint | PRE-LAUNCH TEST | 2026-09-14 20:20:54 BST | — | First watcher prototype. Test-only monitoring; does not start the 30-day experiment. |

## Rules

- Every newly watched market must be added here before or at the same time monitoring begins.
- Every entry must include a full date and time using `Europe/London` and GMT/BST as applicable.
- If monitoring stops, record the removal timestamp rather than deleting the entry.
- Historical entries must remain visible for audit purposes.
- Each market should also have a corresponding detailed file in `market_watch/markets/` once it becomes active or enters formal pre-launch testing.
