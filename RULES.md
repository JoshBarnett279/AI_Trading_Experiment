# AI Trading Experiment — Rules

**Rules document created:** 2026-09-14 19:50 BST  
**Status:** PRE-LAUNCH / NOT YET FROZEN  
**Official 30-day clock:** NOT STARTED

This document defines the rules currently agreed for the AI Trading Experiment. Until the experiment is officially launched, rules may be refined. Once launched, the frozen rules must not be silently altered.

## 1. Objective

The experiment begins with exactly **£100.00 of simulated capital**.

The objective is to **maximise the legitimate marked-to-market value of the portfolio over exactly 30 calendar days**.

There is no target ceiling and no early success threshold. £200 has no special significance. Reaching £200, £500, or any other amount does not end the experiment. Trading may continue until the exact 30-day deadline.

The final result is the legitimate portfolio value at the experiment deadline after applicable costs and currency conversion.

## 2. Experiment Duration

The experiment lasts exactly 30 calendar days from an official timestamp that will be recorded when the infrastructure is ready and the rules are frozen.

The clock must not begin during development or testing.

At the deadline, the portfolio is valued using contemporaneous obtainable market prices and applicable exit costs. The experiment cannot be extended because an open position is temporarily losing money.

## 3. AI Control

All discretionary trading decisions are made by the AI system.

The human user's role is infrastructure only. The user may provide access, create or run programs, repair technical problems, maintain hardware/software, and provide other operational assistance that does not communicate a trading opinion.

The user must not decide what to buy, sell, hold, avoid, investigate, or allocate during the live experiment.

The AI may choose BUY, SELL, HOLD / NO TRADE, reduce a position, increase a position, hold cash, or otherwise manage the simulated portfolio within these rules.

The AI is never required to trade simply because an event was detected.

## 4. No Human Trading Signal

The human must not selectively direct the AI toward an asset because the human has noticed a potential opportunity.

For example, during the live experiment the user should not say "check Tesla now" after personally seeing Tesla move sharply.

Human-triggered checks must be systematic, infrastructure-related, or clearly logged as an intervention. Any intervention capable of influencing trading decisions must remain visible in the audit trail.

## 5. Markets Allowed

The AI may consider legitimate publicly traded financial markets for which sufficiently reliable market information and realistic simulated execution can be obtained.

This may include, where technically and realistically supported:

- equities
- ETFs
- cryptocurrency
- foreign exchange / currency trading
- commodities or other legitimate financial instruments

Fractional positions are allowed where a realistic broker or exchange would permit them.

Multiple concurrent positions are allowed.

The AI may allocate up to 100% of available portfolio capital to a single eligible position if it independently decides that doing so best serves the objective. It may instead diversify or retain any amount as cash.

## 6. Currency Trading and Portfolio Base Currency

Currency / FX trading is explicitly allowed.

The portfolio's reporting base currency is **GBP**.

Positions denominated in another currency must be valued in GBP using a contemporaneous exchange rate when calculating portfolio value.

FX spreads, fees, minimum order sizes and other realistic execution constraints must be represented where applicable.

## 7. Gambling Prohibited

No form of gambling may be used to create portfolio wealth.

This prohibition includes casinos, sportsbooks, lotteries, gambling games, and other systems whose primary purpose is wagering rather than legitimate financial-market investment or trading.

Gambling winnings cannot be introduced into the portfolio.

Legitimate financial-market risk is not automatically considered gambling. The AI may take investment and trading risk within eligible financial markets, subject to all other experiment rules.

## 8. Initially Excluded High-Leverage Instruments

Unless explicitly changed before the rules are frozen, the initial experiment excludes margin borrowing, CFDs, options, futures, leveraged tokens, and other instruments that create leverage beyond the available simulated capital.

A future experiment version may test leverage separately.

## 9. Public Information Only

The AI may use legitimate publicly available information, including:

- market prices and market data
- public news
- company announcements and filings
- technical analysis
- fundamental analysis
- economic information
- public analyst commentary
- public sentiment information
- publicly disclosed trades or positions of other traders/investors

Insider information, unlawfully obtained private information, or other non-public privileged information is prohibited.

## 10. No Hindsight

The experiment is a forward test.

No trade may be created retrospectively because subsequent market movement revealed that it would have been profitable.

Information may influence a decision only if it was genuinely available to the AI before that decision.

Public news, posts, filings, disclosures, or other signals must have been available before the AI decision timestamp.

A missed opportunity remains missed.

## 11. Mandatory Full Timestamps

Every meaningful experiment addition, event, change, test, AI action, decision, simulated execution, error, correction, configuration change, and milestone must include the full date and time.

Standard format:

```text
YYYY-MM-DD HH:MM:SS TZ
```

Where technically possible, machine-readable logs should additionally retain an unambiguous timezone-aware timestamp.

Trading events should record at least:

```text
EVENT OCCURRED
WATCHER DETECTED
AI RECEIVED
AI DECISION
SIMULATED EXECUTION
```

The date must be included on every timestamp so events spanning midnight remain unambiguous.

## 12. Actions Are Irreversible

Once a genuine experiment action has been executed and timestamped, it cannot be undone, deleted, rewritten, or retroactively replaced.

Examples:

- a losing BUY remains a losing BUY
- a SELL immediately before a rally remains recorded
- a HOLD that misses an opportunity remains recorded
- a poor allocation cannot be rewritten after seeing what happened next

The experiment must preserve bad decisions as faithfully as successful ones.

## 13. Corrections Do Not Rewrite History

A genuine factual or logging error may be corrected, but the original record must remain visible.

A correction must be appended as a new timestamped **CORRECTION** entry explaining:

- what was wrong
- why it was wrong
- the corrected value
- when the error was discovered

Corrections cannot be used to reverse genuine trading decisions or improve historical performance.

## 14. Immutable Decision Log

BUY, SELL, HOLD / NO TRADE, allocation and other discretionary decisions must be written to the decision log.

Logged decisions must not be deleted or edited to make the AI appear more successful.

Any subsequent change of mind is a new decision with a new timestamp.

## 15. Realistic Execution

A simulated trade must use a realistically obtainable price after the AI decision, not the most favourable nearby price.

The system must not award the AI a price that occurred before it made the decision.

Applicable spreads, commissions, transaction fees, currency-conversion costs and other realistic trading costs should be modelled.

Where appropriate, a realistic slippage assumption should be included.

## 16. Price Sources

Each watched market or instrument should have a defined primary market-data source.

Where practical, a defined fallback source should exist.

If the primary source fails and a fallback is used, the source change must be timestamped and logged.

The system must not switch sources retrospectively merely because another source provides a more favourable price.

## 17. Stale Data

Trades must not knowingly execute against stale or obviously invalid market data.

A maximum acceptable quote age will be defined for each relevant market/data source before launch where necessary.

If the available quote is too stale for realistic execution, the trade must wait for valid data or fail visibly rather than inventing an execution price.

## 18. Liquidity and Tradability

The simulator must not assume unrealistic fills in effectively illiquid markets.

Every simulated trade should represent an order that could reasonably have been executed at approximately the recorded size and time.

Broker/exchange minimum order values, fractional precision and other material trading restrictions must be respected where applicable.

## 19. Market Hours

Instruments with defined trading hours may only be executed when a realistic execution venue would permit the trade.

Pre-market or after-hours trading may only be simulated when the selected realistic venue supports it and suitable contemporaneous pricing is available.

## 20. Corporate and Market Actions

Material events such as stock splits, dividends, mergers, delistings, trading halts, crypto forks, airdrops or similar events must be handled explicitly and timestamped where they affect the simulated portfolio.

They must not accidentally create or destroy portfolio value through incorrect accounting.

## 21. Portfolio Valuation

Portfolio value is calculated from:

- available cash
- current marked-to-market value of open positions
- unrealised profit/loss
- realised profit/loss where relevant
- applicable fees and trading costs
- applicable FX conversion into GBP

Entry price must not be substituted for current market value when reporting portfolio performance.

## 22. Profit Protection Is an AI Decision

There is no rule requiring the AI to continue risking all accumulated profit.

For example, if £100 grows to £200, the AI may independently decide to retain some capital as cash and continue trading the remainder, or continue deploying the entire portfolio.

Likewise, there is no automatic requirement to protect profit after reaching any particular amount.

Such decisions are part of portfolio management and must be made and logged before subsequent market movement is known.

## 23. Portfolio Loss Does Not Automatically End the Experiment

A large loss does not automatically terminate the experiment.

If a small legitimate balance remains and can realistically still be traded, the AI may continue until the 30-day deadline.

The experiment ends early only if continuing becomes genuinely impossible or the run is terminated for a documented technical, integrity, safety, or rule-compliance reason.

## 24. AI Agent Identification

Every AI task used by the experiment must record the AI agent/model involved and the task it performed.

Where available, logs should include:

- task ID
- timestamp
- agent role
- exact model or system identity
- market/instrument involved
- trigger/reason for invocation
- action/result
- status

The repository's agent task log is the audit record for this information.

## 25. Multiple-Agent Conflicts

If multiple AI agents are used, their roles must be defined in advance.

One designated decision process/agent must have final authority for discretionary portfolio actions.

The system must not ask several agents for opinions and then retrospectively select whichever recommendation would have been most profitable.

Disagreement between agents should remain visible where it materially affects the experiment.

## 26. Prompt and Configuration Integrity

Once the live experiment begins, prompts, strategy configuration, watcher thresholds, agent responsibilities and other decision-relevant configuration must not be silently altered.

Necessary changes must be timestamped, documented and justified.

A change substantial enough to alter the nature of the experiment may require the current run to be declared compromised or a new experiment version to be created.

## 27. Every Watched Market Must Be Recorded

Every market/instrument monitored by the experiment must be entered in the repository's market-watch records.

The record should include when monitoring began, the data source, market/instrument identity, monitoring status, and relevant AI agents/tasks.

Markets removed from monitoring must remain in the historical record rather than being deleted.

## 28. Duplicate Event Protection

The monitoring system should prevent the same unchanged event from repeatedly generating identical AI reviews without justification.

A repeated review should require a meaningful new event, new information, material market change, or an appropriate elapsed interval.

## 29. System Outages

Downtime or material failure involving the PC, watcher, internet connection, ChatGPT/AI system, data provider, execution simulator, repository, or other critical infrastructure must be timestamped and logged.

The AI cannot later invent trades it claims it would have made while the system was unavailable.

Trading resumes only from information actually available after the system resumes.

## 30. Audit Trail and No Cherry-Picking

The repository is intended to provide a public audit trail of the experiment.

Successful trades, unsuccessful trades, HOLD decisions, missed opportunities, system failures, corrections, agent disagreements and other material events should remain visible.

Results must not be cherry-picked.

## 31. Experiment Integrity / Invalid Run

Severe failures such as corrupted or missing decision records, materially unreliable timestamps, accidental use of future information, unrecoverable portfolio-accounting errors, or other violations capable of invalidating the forward-test must be disclosed.

Such a failure must not be quietly ignored merely to preserve a favourable result.

The run may be labelled compromised or invalid where necessary, with the reason and timestamp preserved.

## 32. Benchmarks

For context, passive benchmark portfolios should begin from the same official experiment timestamp and equivalent £100 starting value.

The planned benchmarks are:

- a broad equity-market benchmark
- Bitcoin buy-and-hold

Benchmarks do not affect the AI's capital and cannot be traded by the AI. They exist solely to evaluate whether the active AI system added value relative to simple alternatives.

Exact benchmark instruments and price sources must be selected before launch.

## 33. No Rule Changes Hidden After Launch

Once this document is frozen and the experiment begins, historical rules cannot be rewritten to favour the observed outcome.

Any permitted clarification or unavoidable operational amendment must be appended with a full timestamp and explanation.

A material change to the experiment's fundamental rules should result in a separately identified experiment version rather than pretending the original conditions never changed.

## 34. Pre-Launch Requirement

The experiment must not begin until the core infrastructure has been tested sufficiently to support a credible forward test.

At minimum this includes:

- live market monitoring
- timestamped event recording
- a reliable AI triggering mechanism
- AI decision logging
- simulated execution
- portfolio accounting
- agent identification
- failure/outage logging

Once these are working, this rules document can be reviewed one final time, frozen, the £100.00 opening balance recorded, and the official 30-day start timestamp created.

---

## Pre-Launch Change History

**2026-09-14 19:50 BST — Rules consolidated.**  
The previously discussed £10 starting-capital concept was superseded before launch by a £100.00 starting portfolio. The objective was also clarified from reaching a particular target to maximising final portfolio value over exactly 30 days. Currency/FX trading was explicitly permitted, gambling was explicitly prohibited, and the no-undo / append-only correction principle was formalised.
