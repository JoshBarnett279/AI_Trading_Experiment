# Trigger bridge — first local step

Pre-launch only. Desktop delivery is not connected or proven. No background
process or schedule has been installed. The original watcher is unchanged.

`bridge.py` reads the watcher's JSONL event format and appends one fixed
`AUTOMATED TEST 001` message per unique test BTC-GBP event to a separate outbox.
It preserves source records and records Europe/London time with BST/GMT and
an ISO offset. Queueing is explicitly labelled `QUEUED_NOT_DELIVERED`.
Only one collector may run at a time in this prototype. The outbox is an
append-only record, not a tamper-proof store. Malformed records stop collection;
an unfinished source line waits for completion. An unfinished outbox requires
inspection; do not erase it.

Run `python -B -m unittest discover -s trigger_bridge -v` from the workspace.
Run `python -B trigger_bridge/probe_watcher.py` for an isolated test of the
original watcher's event branch with synthetic prices and times. This does not
contact the market endpoint or write to the real watcher project. Evidence and
an append-only test audit are saved in `test_evidence`.

Immediate desktop investigation:
- Installed app registers the `codex` URI scheme; its manifest alone does not
  establish a supported send-prompt URI.
- Hooks respond to agent lifecycle events, not arbitrary incoming file events:
  https://learn.chatgpt.com/docs/hooks
- App Server documents a programmable Codex interface, but this does not itself
  establish delivery into the running desktop conversation:
  https://learn.chatgpt.com/docs/app-server
- Installed bundled codex.exe could not be executed, including with an escalated
  request. No standalone codex command was found on PATH.
- User chose continued immediate-delivery investigation over scheduled polling.

Next: establish a supported immediate transport and verify an actual desktop
receipt before marking delivery successful. Do not infer AI receipt from
queueing or launching an application. The 30-day clock remains stopped.
