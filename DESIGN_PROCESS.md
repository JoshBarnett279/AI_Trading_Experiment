# AI Trading Experiment — Design Process

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
