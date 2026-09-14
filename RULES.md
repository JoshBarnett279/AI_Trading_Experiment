# AI Trading Experiment — Rules

**Rules document created:** 2026-09-14 19:50 BST  
**Latest pre-launch approval:** 2026-09-14 19:55 BST  
**Status:** PRE-LAUNCH / APPROVED RULESET / NOT YET FROZEN  
**Official 30-day clock:** NOT STARTED

This document defines the approved rules for the AI Trading Experiment. The rules will be frozen immediately before the official experiment begins. After launch, historical rules cannot be silently changed.

## 1. Objective and Capital

The experiment begins with exactly **£100.00 simulated capital**. The objective is to maximise the legitimate marked-to-market GBP value of the portfolio over exactly **30 calendar days**. There is no target ceiling or early-success threshold. Reaching £200, £500, or any other amount does not end the experiment.

No additional external capital may enter the portfolio after launch. Deposits, gifts, promotional credits, gambling winnings or other outside additions are prohibited.

The experiment cannot be restarted because of poor performance and cannot be extended because an open position is losing at the deadline.

## 2. Duration and Final Result

The 30-day clock begins only after the infrastructure is tested, this ruleset is frozen, the £100 opening balance is recorded and an official start timestamp is created.

At the exact deadline, the portfolio is valued using contemporaneous realistically obtainable market prices, applicable exit costs and contemporaneous FX conversion into GBP. The complete portfolio, trade history and audit logs are preserved.

Results will include at least final GBP value, GBP profit/loss, percentage return and maximum drawdown.

## 3. London Time Standard

**Europe/London is the authoritative timezone for the entire experiment.**

Human-readable timestamps must use London local time and automatically follow UK daylight-saving changes, displaying **GMT or BST as applicable on that date**. The system must use the IANA timezone `Europe/London` rather than permanently assuming either GMT or BST.

Standard human-readable format:

```text
YYYY-MM-DD HH:MM:SS GMT/BST
```

Machine-readable records should additionally retain an unambiguous timezone-aware timestamp where technically possible. All system clocks should be synchronised to a reliable time source.

## 4. AI Control

All discretionary trading decisions are made by the AI system. The human user's role is infrastructure only: providing access, running programs, repairing technical problems and maintaining the system without communicating a trading opinion.

The user must not decide what to buy, sell, hold, avoid, investigate or allocate during the live experiment. The AI may independently BUY, SELL, HOLD / NO TRADE, increase/reduce positions or hold cash. A trigger never forces a trade.

## 5. No Hidden Human Trading Signal

The human must not selectively direct the AI toward an asset because the human has noticed an opportunity. Systematic checks and infrastructure assistance are allowed. Any human intervention capable of affecting trading decisions must be visibly logged.

## 6. Allowed Markets and Methods

Where reliable data and realistic simulated execution are available, the AI may use legitimate publicly traded markets including equities, ETFs, cryptocurrency, FX/currency trading and legitimate commodity exposure that does not violate the derivative/leverage rules.

Permitted analytical/trading methods include public news/event analysis, momentum, mean reversion, technical analysis, fundamental analysis, sentiment analysis, public trader/investor disclosures, cross-market signals, relative-value analysis, earnings analysis, arbitrage detection where genuinely executable, dynamic position sizing, cash management, fixed stop-losses and trailing stops.

Crypto may be monitored/traded when its market is open, including 24/7 markets. FX may be monitored/traded during realistically available FX trading sessions.

The monitoring system may dynamically identify new instruments rather than being restricted to a fixed asset list, provided every actually monitored market is logged.

## 7. Capital Constraint: Trade Only What We Own

The AI may trade only with capital or assets currently owned by the simulated portfolio.

It may never borrow money, borrow securities/assets, create a negative cash balance or obtain exposure exceeding available portfolio resources.

Therefore **margin, leverage, conventional short selling, borrowed shares, CFDs, options, futures, leveraged tokens and similar leveraged/borrowed instruments are prohibited**.

An attempted order exceeding available resources must be rejected mechanically and the rejection timestamped and logged.

Fractional positions are allowed only where the assumed realistic venue supports them. Multiple concurrent positions are allowed. Up to 100% of available portfolio capital may be allocated to one eligible position if the AI independently judges that appropriate.

## 8. Gambling Prohibited

No gambling may be used to create portfolio wealth. This includes casinos, sportsbooks, lotteries, gambling games, prediction-market wagering and similar mechanisms whose primary purpose is wagering rather than legitimate financial-market investment/trading. Gambling winnings cannot enter the portfolio.

Legitimate financial-market risk is allowed, but a financial instrument cannot be used merely as a disguised lottery. A highly concentrated or speculative position requires a documented evidence-based market thesis rather than an all-or-nothing hope of an extreme payout.

## 9. Public Information Only

The AI may use legitimate publicly available market prices/data, news, company announcements/filings, technical analysis, fundamentals, economic data, analyst commentary, public sentiment and publicly disclosed trades/positions.

Insider information, unlawfully obtained private information and other non-public privileged information are prohibited.

Information may influence a decision only if it was genuinely available before the AI decision timestamp.

## 10. No Hindsight

This is a forward test. No trade may be created retrospectively because subsequent movement showed it would have been profitable. The AI cannot claim a trade at an earlier time than it actually received and processed the relevant information. Missed opportunities remain missed.

## 11. Mandatory Event Timestamps

Every meaningful event, addition, change, test, AI task, decision, execution, error, correction, configuration change, outage and milestone receives a full Europe/London timestamp.

Trading events record at least:

```text
EVENT OCCURRED
WATCHER DETECTED
AI RECEIVED
AI DECISION
SIMULATED EXECUTION
```

The earliest valid trade is after the AI actually receives/processes the event.

## 12. Actions Are Irreversible

Once a genuine experiment action is executed and timestamped, it cannot be undone, deleted, rewritten or retroactively replaced. Losing BUYs, poor SELLs, missed HOLDs and bad allocations remain part of the experiment.

There is no undo button for genuine decisions.

## 13. Corrections Are Append-Only

A genuine factual, software or logging error may be corrected, but the original record remains visible. A new timestamped `CORRECTION` record must state what was wrong, why, the corrected value and when the error was discovered.

Corrections cannot reverse genuine trading decisions or improve historical performance.

## 14. Immutable Decision and Rationale Records

BUY, SELL, HOLD / NO TRADE, allocation and other discretionary decisions are logged and cannot be edited after subsequent market movement is known.

Every discretionary executed trade must have a short linked rationale created before or at the decision. It should record at least:

- unique trade ID
- Europe/London decision timestamp
- asset and action
- position size
- concise evidence-based reason
- relevant event/task references
- AI agent/model
- initial risk/exit plan
- re-entry status and previous trade ID where applicable

SELL decisions receive a short rationale as well. Automatic stop executions link to the rationale that established the stop. Rationale records are immutable after execution; later observations/corrections are appended separately and must never introduce retrospective reasoning into the original rationale.

## 15. Stop-Loss and Trailing-Stop Rules

Fixed and trailing stops are allowed. Protective stops should normally be considered when a position is opened or materially increased, but a stop is not mandatory where the AI has a documented reason that it is inappropriate.

A new protective stop cannot be invented or tightened merely to retrospectively protect an already failing trade. The AI may still make a fresh discretionary SELL decision on a losing position.

A stop may move in the position's favour according to its legitimate trailing/protection logic. Moving a stop further into loss requires a new documented evidence-based justification and cannot be done merely to avoid accepting a losing trade.

A stop's trigger price is not a guaranteed execution price. The simulator uses a realistically obtainable price after triggering, including gaps/slippage where applicable.

## 16. Re-entry After a Loss or Stop

An asset may be bought again after a loss or stop only following fresh AI analysis with a specific evidence-based reason. Re-entry cannot be motivated solely by recovering the previous loss, an unsupported hunch or the fact that the asset is now cheaper.

There is no arbitrary cooldown period. Genuine new information or a genuinely new setup can justify rapid re-entry.

Every reopened trade is a new trade with a new ID, new rationale, new risk assessment and new stop decision where appropriate. There must be no automatic `stop -> rebuy -> stop -> rebuy` loop.

## 17. Realistic Execution

Simulated trades use realistically obtainable prices after the AI decision, never the most favourable nearby chart price. Applicable spreads, commissions, transaction fees, FX fees and realistic slippage are modelled where relevant.

Broker/exchange minimum order sizes, fractional precision and material restrictions must be respected. The simulator cannot assume unrealistic fills in effectively illiquid markets.

Every simulated order receives a unique order ID. Duplicate messages must not execute the same order twice.

## 18. Price Sources and Stale Data

Each watched instrument has a defined primary market-data source and, where practical, a fallback. Source changes are timestamped. Sources cannot be switched retrospectively to obtain a favourable price.

Maximum acceptable quote age will be defined by market/data source before launch where needed. Stale, invalid or unreliable data cannot be used for execution. If trustworthy market data is unavailable, the trading system **fails closed** and does not invent prices or trades.

## 19. Liquidity, Market Hours and Tradability

Orders must represent trades that could reasonably have executed at approximately the recorded size/time. Market hours and realistic venue restrictions are respected. Extended-hours trading is allowed only when the assumed venue supports it and suitable contemporaneous pricing is available.

## 20. Corporate and Market Actions

Dividends, splits, mergers, delistings, trading halts, crypto forks, airdrops and similar material events are explicitly accounted for where they affect the portfolio. They cannot accidentally manufacture or destroy simulated wealth through incorrect accounting.

External benefits such as promotional credits or referral bonuses do not count. Dividends, interest, staking income or comparable returns count only when they would genuinely have accrued to the simulated position under the assumed venue/product during the experiment.

## 21. GBP Portfolio Valuation

GBP is the portfolio reporting currency. Portfolio value includes cash, current marked-to-market open positions, realised/unrealised P&L, fees/costs and contemporaneous FX conversion.

Foreign-currency positions use contemporaneous FX rates. Entry price cannot substitute for current market value when reporting performance.

Portfolio accounting must reject impossible states such as spending more cash than is available.

## 22. Profit Protection Is an AI Decision

There is no automatic requirement to risk or protect a particular amount after making profit. If £100 becomes £200, the AI may retain some as cash or continue deploying it. The decision must be made prospectively and logged before subsequent movement is known.

## 23. Loss Does Not Automatically End the Experiment

A large loss does not automatically terminate the run. If a legitimate tradable balance remains, the AI may continue until the deadline. The experiment ends early only if continuation becomes genuinely impossible or a documented technical/integrity/rule-compliance issue requires termination.

## 24. AI Agent Identification and Specialist Agents

Multiple specialist AI agents may be used for areas such as news, technical analysis, macro/FX, crypto and risk. Every AI task records the responsible model/agent, role, timestamp, trigger, market, result and status where available.

Specialist agents provide analysis. One predetermined decision process/agent has final discretionary portfolio authority. Agent opinions cannot be cherry-picked retrospectively according to which would have been profitable.

## 25. Opportunity Scoring and Monitoring

Mechanical watchers may score/prioritise potential opportunities using objective inputs such as price movement, volume, volatility, news significance and sentiment. Such scores decide what deserves AI review, not whether a trade is executed.

A separate risk-monitoring process may watch existing positions and trigger AI reassessment when material risk conditions change.

Duplicate triggers should be suppressed unless there is meaningful new information, material market change or an appropriate elapsed interval.

## 26. Prompt and Configuration Integrity

After launch, prompts, thresholds, strategy configuration, agent roles and decision-relevant logic cannot be silently altered. Necessary changes must be timestamped, documented and justified. A material change may require the run to be declared compromised or moved to a new experiment version.

## 27. Market Registry

Every market/instrument actually monitored is entered into the market-watch records with relevant source, status and timestamps. Instruments removed from monitoring remain historically visible.

## 28. System Outages

Downtime or material failure involving the PC, watcher, internet, AI system, market-data provider, execution simulator, repository or other critical infrastructure is timestamped and logged.

No hypothetical trades may later be reconstructed for periods when the AI/system was unavailable. Trading resumes only from information genuinely available after recovery.

## 29. Audit Trail and Git Integrity

Successful trades, losing trades, HOLDs, missed opportunities, system failures, rejected orders, corrections, agent disagreements and other material events remain visible. Results cannot be cherry-picked.

GitHub commit history forms part of the audit trail and must not be rewritten to conceal mistakes.

## 30. Experiment Integrity / Invalid Run

Severe corruption/missing decision records, materially unreliable timestamps, future-information contamination, unrecoverable accounting errors or comparable violations must be disclosed rather than hidden. The run may be labelled compromised or invalid where necessary, with the reason and timestamp preserved.

## 31. Benchmarks

Passive benchmarks begin at the same official timestamp with equivalent £100 starting values. At minimum these will include a broad equity-market benchmark and Bitcoin buy-and-hold. Exact benchmark instruments and data sources will be selected before launch.

Benchmarks are observational only and never interact with the AI's £100 portfolio.

## 32. Automated Scoring

Wherever practical, final performance and portfolio accounting are calculated mechanically from the immutable ledger rather than allowing the AI to manually determine its own score.

## 33. No Hidden Rule Changes After Launch

Once frozen and launched, historical rules cannot be rewritten to favour observed results. Any unavoidable clarification/amendment is appended with a Europe/London timestamp and explanation. A material change becomes a separately identified experiment version rather than pretending the original conditions never changed.

## 34. Pre-Launch Requirement

The experiment cannot begin until the core infrastructure has been tested sufficiently for a credible forward test, including:

- live market monitoring
- timestamped event recording
- reliable AI triggering
- AI decision and rationale logging
- simulated execution
- portfolio accounting
- unique order/trade IDs and duplicate protection
- agent identification
- risk monitoring
- outage/failure logging
- trustworthy London-time timestamping

Only after these pass testing will this ruleset be frozen, the £100.00 opening balance recorded and the official 30-day start timestamp created.

---

## Pre-Launch Change History

**2026-09-14 19:50 BST — Initial consolidated rules.**  
The earlier £10 concept was superseded before launch by £100.00. The objective became maximising final portfolio value over exactly 30 days. FX was permitted, gambling prohibited and the no-undo/append-only correction principle formalised.

**2026-09-14 19:55 BST — Expanded rules approved.**  
All additional rules reviewed in the pre-launch discussion were approved. The capital constraint was strengthened to prohibit borrowing money or assets, leverage and conventional short selling. Options, futures, CFDs and other leveraged/borrowed instruments were prohibited. Trade rationale records, stop-loss/trailing-stop protections, evidence-based re-entry rules, fail-closed market data, unique order IDs, automated accounting safeguards, maximum-drawdown reporting and Git audit integrity were added. **Europe/London was designated as the authoritative experiment timezone, automatically using GMT/BST as applicable.**
