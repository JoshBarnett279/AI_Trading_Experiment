# ChatGPT bridge — production candidate, PRE-LAUNCH

This one-shot adapter is separate from the running watcher. The 30-day clock
has not started, rules remain unfrozen, and no trades or decisions are executed.
It accepts the existing watcher's MARKET_EVENT shape with test_mode=true,
product=BTC-GBP, event_id and offset-aware watcher_detected_iso. Extra fields
are preserved as data. It does not tail market_events.jsonl or install a service.

## First small test

In the repository directory, with the dedicated Chrome already running on
127.0.0.1:9222, run:

```bat
python chatgpt_bridge.py --list-targets
```

This only lists open conversation URLs and titles. Identify the URL belonging
to **Trading Experiment Live Bridge**. The prior setup preview did not expose
its complete URL, so no target has been guessed or silently configured.

## Subsequent isolated validation

Requires Python 3.12, Selenium (development environment: 4.49.0), matching
Chrome/ChromeDriver, and tzdata on Windows. Install dependencies with
`python -m pip install -r requirements-chatgpt-bridge.txt` if needed.
Chrome must already have an authenticated session. Selenium attaches to the
existing browser; it never launches a new profile or navigates to a guessed chat.

Use `python chatgpt_bridge.py --check-target --target-url "EXACT_URL"` to check
the selected tab and empty composer without typing. Exactly one matching tab
is required. Title is informational; full validated URL is the identity.

For a later explicitly chosen isolated send, create a new JSON file containing
one synthetic MARKET_EVENT with a unique event_id, test_mode=true,
product=BTC-GBP and a real offset-aware watcher_detected_iso. Mark synthetic
values clearly. Then use `python chatgpt_bridge.py --event test-event.json
--target-url "EXACT_URL"` on one command line. This command automatically sends.
The message requests acknowledgment only and explicitly retains PRE-LAUNCH.
Do not connect a watcher until the isolated bridge test is reviewed.

## Audit and duplicate protection

`chatgpt_bridge_state/ledger.sqlite3` is the authoritative durable ledger,
stored relative to this script regardless of working directory. Preserve it,
back it up while the bridge is stopped, and use only this installation/state
for delivery. A different copy or deleted ledger defeats duplicate protection.
`python chatgpt_bridge.py --export-audit` prints its append-only audit as JSONL.

BRIDGE RECEIVED retains the source event and normalized WATCHER DETECTED time.
Every audit row includes full Europe/London local date/time with BST/GMT and
microsecond ISO time with an offset. CHATGPT SUBMITTED is recorded only after
the exact sent text appears in a visible user message. Its time is when that
DOM evidence was observed, not the exact server receipt time or AI RECEIVED.
Clock accuracy depends on Windows clock synchronization.

A transactional unique event claim is committed before browser interaction.
Same ID and payload cannot send again, including across concurrent runs and
restarts. Changed payload or target for an existing ID is rejected. Any failure
after reservation remains blocked, even if it occurred before Enter. Inspect
the chat, draft and audit manually; never delete a claim or use a new ID merely
to bypass uncertain delivery. There is deliberately no automatic retry/reset.
This favors at-most-one send attempt over guaranteed delivery; Selenium cannot
provide exactly-once server delivery. The append-only audit is not tamper-proof.
An exclusive ledger.lock also serializes different events using this installation.
A crash can leave that lock behind: stop all bridge processes and inspect the
chat and ledger before manually removing only the stale lock. Retain all claims.

An existing draft, duplicate target tabs, wrong URL, generating response, or
missing composer stops sending. The target is checked before insertion and
Enter. Do not interact with the dedicated tab during a bridge attempt; external
navigation can race browser commands. UI selector changes can cause failure.
The driver service is stopped on exit without quitting dedicated Chrome.

## Evidence and validation

The September 14 archive at
`simulation_tests/2026-09-14_trigger_bridge/` remains historical queue-only
evidence. No archived file was modified by this addition.

On September 15 the user reported successful insertion of BRIDGE TARGET TEST
001 and then confirmed automatic submission in the AI trading experiment
conversation (6aa831a8-a840-83eb-8cd8-9afb05a75036). This proves the reported
manual-command Python -> Selenium -> dedicated Chrome -> correct composer ->
automatic submission path. It does not prove this new adapter or watcher
integration. Exact browser submission time is unavailable and is not invented.
See `chatgpt_bridge_audit.jsonl` for provenance and recording timestamps.

Offline tests: `python -B -m unittest discover -p test_chatgpt_bridge.py -v`.
They cover durable restart deduplication, uncertain delivery, ID collisions,
shared ledger claims, event restrictions, URL validation and BST/GMT. Browser
transport still needs the isolated test on the user's dedicated Chrome.


## Isolated validation update — 2026-09-15 20:42:46 BST

Automatic submission and duplicate blocking passed on 15 September 2026.
See simulation_tests/2026-09-15_chatgpt_bridge/ for the actual audit and results.
This supersedes the earlier pending isolated-test status above. Watcher
integration remains disconnected and the experiment remains PRE-LAUNCH.


## Controlled integration update — 2026-09-15 22:36:14 BST

Controlled synthetic file -> follower -> real ChatGPT delivery and duplicate
blocking passed. The initial Show more confirmation timeout and its fix are
preserved in simulation_tests/2026-09-15_controlled_connector/. 22 offline
tests pass. Natural market-event delivery remains untested; PRE-LAUNCH remains.
