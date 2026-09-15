# AI Trading Experiment — Design Process

**Document created:** 2026-09-14 (UK time)

## Documentation Timestamp Standard

**Added: 2026-09-14 19:37:42 BST**

From this point onward, every addition, change, experiment entry, design decision, trade decision, program-generated event, and other meaningful record should include a timestamp.

Standard format:

```text
YYYY-MM-DD HH:MM:SS TZ
```

Example:

```text
2026-09-14 19:37:42 BST
```

The full date must be recorded so that entries remain unambiguous when development or trading crosses into a new day. Automated components should generate timestamps themselves rather than relying on manually entered times wherever possible. Trading-related records should additionally preserve the relevant event, detection, receipt, decision, and execution timestamps described below.

## Purpose

This document records how the AI Trading Experiment is designed, tested, and refined before the official 30-day forward-test begins.

The goal is not only to see whether an AI-controlled simulated £10 portfolio can reach £20, but also to build an auditable technical system that could be useful later as a portfolio project, learning record, or basis for a more advanced personal project.

## Core Principle

The experiment must be genuinely forward-tested.

No trade may be claimed after the fact using information that was not available to the AI at the time of the decision. Every market event, AI review, decision, and simulated execution should be timestamped.

## Initial Challenge Definition

- Starting capital: £10.00 simulated cash
- Target portfolio value: £20.00
- Planned duration: 30 calendar days from the official start timestamp
- User role: infrastructure only, not trading decisions
- AI role: trading decisions and portfolio management
- Market scope: broad, using legitimate public information and realistic execution assumptions

The official experiment clock will not begin until the monitoring, triggering, decision, and logging system has been tested.

## Proposed System Architecture

The current target architecture is:

```text
Live market data / news / public signals
            ↓
Local market watcher
            ↓
Timestamped event store
            ↓
AI trigger
            ↓
AI reviews current information
            ↓
BUY / SELL / HOLD decision
            ↓
Simulated execution
            ↓
Portfolio ledger + audit log
```

## Why a Local Watcher

ChatGPT itself should not be described as continuously monitoring markets when it is not actively invoked.

A local program running on the user's PC can remain active 24/7 and monitor prices, news, volatility, or other signals much more frequently than a scheduled ChatGPT task.

The watcher is intended to perform inexpensive mechanical work such as:

- collecting live prices
- checking percentage moves
- detecting unusual volume or volatility
- collecting relevant news/events
- recording timestamps
- deciding when an event is important enough to request an AI review

The watcher should not make discretionary trading decisions unless the design is deliberately changed later.

## Trigger Problem

The main unresolved engineering problem is how the local watcher should invoke the AI immediately after a significant event.

Possible approaches considered:

1. **OpenAI API**
   - clean and reliable software-to-software communication
   - allows immediate event-driven AI calls
   - incurs separate API usage costs

2. **ChatGPT desktop app automation**
   - potentially uses the existing ChatGPT subscription
   - local watcher could trigger a message to the desktop app
   - needs to be tested for reliability and whether a supported background mechanism exists

3. **Windows UI automation**
   - program could bring ChatGPT to the foreground and submit a fixed review command
   - potentially zero additional AI cost
   - more fragile and may interfere with normal computer use

The preferred path is currently to investigate whether the ChatGPT desktop environment can be triggered cleanly before paying for API usage.

## Desktop Environment Findings

The ChatGPT desktop app exposes settings including:

- Hooks
- Connections
- Git
- Environments
- Worktrees
- Computer use

At the time of inspection:

- Hooks showed no existing hooks
- Connections appeared focused on device/SSH connectivity rather than arbitrary market-event triggers
- Full Access was left disabled until there is a concrete need for it

The desktop app may still be useful because the user's PC can remain on continuously with ChatGPT running or minimized.

## Timing and Anti-Hindsight Rules

Each event should eventually record at least:

```text
EVENT OCCURRED
WATCHER DETECTED
AI RECEIVED
AI DECISION
SIMULATED EXECUTION
```

Example:

```text
EVENT OCCURRED:      18:32:14
WATCHER DETECTED:     18:32:16
AI RECEIVED:          18:32:21
AI DECISION:          18:32:29
SIMULATED EXECUTION:  18:32:30
```

The earliest valid simulated trade price is after the AI has actually received and processed the event.

## Planned Audit Rules

The experiment is intended to follow these principles:

- decisions are immutable once logged
- corrections are added as new records rather than rewriting history
- bad trades and missed opportunities remain visible
- execution prices should use a realistic obtainable price after the decision
- spreads and fees should be modelled where relevant
- no insider or private information
- public news, market data, technical analysis, fundamentals, sentiment, and publicly disclosed trades may be considered
- the human may stop the experiment, but should not intervene to rescue a losing position
- rule changes after launch should create a new experiment version rather than silently changing the live rules

## Proposed Repository Structure

```text
AI_Trading_Experiment/
├── watcher/
│   ├── market_watcher.py
│   └── news_watcher.py
├── data/
│   └── market_events.jsonl
├── portfolio/
│   ├── ledger.csv
│   └── positions.json
├── decisions/
│   └── decisions.jsonl
├── config/
│   └── strategy.json
├── DESIGN_PROCESS.md
├── RULES.md
└── README.md
```

This structure is provisional and can be refined before launch.

## Development Plan

Before the 30-day clock starts, the system should pass the following stages:

1. Build a basic local watcher.
2. Prove that it can collect and timestamp live data.
3. Build an event threshold/filter so the AI is not invoked unnecessarily.
4. Prove that a significant event can trigger an AI review automatically.
5. Build the simulated execution engine.
6. Build the portfolio ledger.
7. Test failure handling, including app closure, lost internet, and stale prices.
8. Freeze the final experiment rules in `RULES.md`.
9. Record the £10.00 opening balance and official start timestamp.
10. Begin the 30-day forward-test.

## Current Status

**Pre-launch architecture stage.**

GitHub connectivity from ChatGPT has been confirmed. The repository can be read and written by the connected ChatGPT GitHub integration.

The next technical milestone is to test whether a local program can reliably invoke the ChatGPT desktop app while it is running or minimized. If that cannot be made robust, an API-based AI trigger will be evaluated as the fallback.

## Portfolio / Career Value

This project can demonstrate practical experience with:

- event-driven software design
- API and live-data integration
- automation
- Python development
- Git/GitHub version control
- audit logging and reproducibility
- systems thinking
- handling latency and failure states
- AI-agent integration
- quantitative experiment design

The experiment result itself is less important than the quality, transparency, and technical rigor of the system used to run it.

---

This file should be updated throughout development so that design decisions, failures, changes, and reasoning remain visible in the repository history.

## 2026-09-15 PRE-LAUNCH design catch-up

**Added: 2026-09-15 05:29:22 BST**

This section is additive and preserves the earlier design record above. Where the original concept above says £10/£20, that is historical design context only. `RULES.md` later superseded it before launch with exactly **£100.00 simulated capital**, GBP reporting/base currency, and a 30-day objective. The rules remain PRE-LAUNCH / NOT YET FROZEN and the official clock remains **NOT STARTED**.

### Status vocabulary

- **IMPLEMENTED**: code/documentation exists in the repository.
- **TESTED**: observed in a recorded pre-launch test; this does not imply production readiness.
- **PLANNED**: agreed design direction, not yet demonstrated end-to-end.
- **UNCONFIRMED**: evidence is insufficient to state a cause or capability.

### Watcher progress

**Recorded: 2026-09-15 05:29:22 BST**

- **IMPLEMENTED + TESTED:** Windows watcher collected real Coinbase `BTC-GBP` spot observations and timestamped them in `Europe/London`.
- **IMPLEMENTED + TESTED:** polling interval is 15 seconds and the watcher calculates movement against a rolling 300-second (5-minute) lookback.
- **IMPLEMENTED, TEST ONLY:** the current trigger is ±0.5% over 5 minutes. It is an engineering threshold, not a frozen trading rule. Before launch it should be replaced/tuned using smarter multi-window filtering, potentially including volatility, volume, news significance and portfolio context.
- **TESTED:** an isolated synthetic bridge test generated a watcher event and converted it to a deduplicated local message queue. Automatic ChatGPT receipt/delivery remains unproven.

### Windows timezone dependency

**Recorded: 2026-09-15 05:29:22 BST**

During Windows testing, `zoneinfo` could not obtain the IANA timezone database. Installing the Python `tzdata` package resolved the issue:

```text
python -m pip install tzdata
```

`tzdata` is therefore an explicit runtime dependency for portable Windows use even though some operating systems provide timezone data themselves.

### Unexpected watcher/CMD closure

**Recorded: 2026-09-15 05:29:22 BST**

**UNCONFIRMED:** during testing the watcher/CMD window unexpectedly closed. Windows Event Viewer showed no relevant Application crash. A separate Ctrl+C test stopped Python but did **not** close CMD. Accidental manual closure is possible, but there is not enough evidence to identify the cause and no cause should be invented.

**PLANNED launch requirement:** persistent error/crash logging plus automatic recovery/restart must exist and be failure-tested before launch.

### AI/token-efficiency architecture

**Decision recorded: 2026-09-15 05:29:22 BST**

**PLANNED:** routine monitoring, timestamping, logging, threshold calculations and filtering happen locally without AI usage. Events are filtered and deduplicated before any AI invocation. The local system sends compact event packets containing only the decision-relevant context. AI is reserved for meaningful analysis and discretionary BUY/SELL/HOLD decisions. If AI access is unavailable, the system fails safely and records the condition; it must not attempt to circumvent product/API usage limits.

### Simulated portfolio and execution engine

**Decision recorded: 2026-09-15 05:29:22 BST**

**PLANNED:** build and dry-run a mechanical simulator using exactly **£100.00 PRE-LAUNCH test cash** with GBP as base/reporting currency. It will support BUY, SELL and HOLD; unique order IDs; append-only immutable decision/order/execution records; realistic obtainable prices after decisions; configurable spread, fees and slippage; no borrowing, leverage or shorting; mechanical rejection/logging of impossible orders; and deterministic portfolio accounting. The £100 pre-launch test balance is test state only and is not the official opening balance/start event.

### Persistent prospective orders and offline reconciliation

**Decision recorded: 2026-09-15 05:29:22 BST**

**PLANNED:** stop-loss and take-profit/limit orders that were genuinely established prospectively may remain active while the PC is off. No retrospective AI decision may be inserted into downtime. On restart, trustworthy historical data will be used to determine whether a pre-existing order actually triggered, then simulate a realistic fill. Records must keep the historical market event/execution timestamp separate from the later reconciliation timestamp.

### PREPARE FOR SHUTDOWN / RESUME EXPERIMENT

**Decision recorded: 2026-09-15 05:29:22 BST**

**PLANNED:** `PREPARE FOR SHUTDOWN` will refresh data, allow an AI review of current positions, establish any appropriate prospective orders, validate and persist state, and only then confirm `SAFE TO SHUT DOWN`. `RESUME EXPERIMENT` will reconcile downtime, process only orders that genuinely existed before shutdown, update accounting, log the downtime/reconciliation, and restart monitoring. Neither workflow permits hindsight.

### Health watchdog and human intervention boundary

**Decision recorded: 2026-09-15 05:29:22 BST**

**PLANNED:** critical components will emit timestamped heartbeats. Stale heartbeats, not “no trades for an hour,” are the primary failure signal because legitimate inactivity/HOLD periods are possible. A stale heartbeat creates a technical-intervention alert and audit record. Human intervention may repair infrastructure but may not make, cancel or modify trading decisions.

### Phone failure-notification test

**Decision recorded: 2026-09-15 05:29:22 BST**

**PLANNED / UNCONFIRMED capability:** deliberately simulate a watcher/heartbeat failure while the user is away from the conversation and determine whether the automated ChatGPT workflow produces the normal ChatGPT mobile push notification. Do not assume this works until demonstrated. If it is unreliable, a separate reliable phone-alert mechanism is required before launch.

### Updated remaining development sequence

**Roadmap updated: 2026-09-15 05:29:22 BST**

1. Automatic event → ChatGPT triggering and receipt proof.
2. Simulated £100 portfolio.
3. Execution engine.
4. Persistent prospective orders.
5. Shutdown preparation workflow.
6. Restart/downtime reconciliation.
7. Health watchdog and phone-notification path.
8. Failure testing, including persistent logging and automatic recovery.
9. Final watcher/filter tuning, replacing the ±0.5%/5-minute TEST ONLY threshold as appropriate.
10. Complete end-to-end dry run.
11. Final rules review and freeze.
12. Record the official £100.00 opening balance and official start timestamp.
13. Begin the 30-day experiment.

**Checkpoint: 2026-09-15 05:29:22 BST — PRE-LAUNCH. Official 30-day clock NOT STARTED.**
