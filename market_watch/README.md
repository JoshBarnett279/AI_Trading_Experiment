# Market Watch Audit Folder

Created: 2026-09-14 19:40:02 BST

This folder records every market, asset, or instrument monitored during the AI Trading Experiment and identifies which AI agent/model was used for each individual task.

## Purpose

The goal is full traceability. At any point, it should be possible to answer:

- What markets were being watched?
- When was each market added or removed?
- What data source was used?
- Which AI agent/model handled each task?
- What task did that agent perform?
- What market/event/decision did the task relate to?
- When did the task occur?

## Folder Structure

```text
market_watch/
├── README.md
├── MARKET_REGISTRY.md
├── AGENT_TASK_LOG.csv
└── markets/
    └── README.md
```

## Logging Standard

Every meaningful addition must include a full timestamp using:

`YYYY-MM-DD HH:MM:SS TZ`

Example:

`2026-09-14 19:40:02 BST`

If the calendar day changes, the new date must be recorded explicitly. No time-only entries are permitted.

## Agent Identification Standard

For every AI-assisted task, record both:

- **Agent role/name**: e.g. ChatGPT trading decision agent, market triage agent, news analysis agent
- **Model**: e.g. GPT-5.6 Sol, local model name, or other external AI model

If multiple agents contribute to one task, each contribution should receive its own task-log entry.

## Market Files

Once monitoring begins, each watched market/asset should receive its own file inside `markets/` containing its monitoring history, relevant sources, trigger events, AI reviews, and status changes.

No markets are active yet. The experiment remains in the pre-launch architecture stage.
