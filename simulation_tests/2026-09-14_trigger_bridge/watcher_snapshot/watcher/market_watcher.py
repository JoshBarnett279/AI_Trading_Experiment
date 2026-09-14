"""
AI Trading Experiment - Market Watcher Prototype
Created: 2026-09-14 20:20:54 BST
Status: PRE-LAUNCH TESTING ONLY

Purpose:
- Fetch BTC-GBP spot price from a public market-data endpoint.
- Timestamp observations using Europe/London.
- Append observations to JSONL.
- Detect a configurable percentage move over a configurable lookback window.
- Create unique event IDs.
- Suppress duplicate/repeated alerts with a cooldown.

This script does NOT place trades, make trading decisions, or start the 30-day experiment.
"""

from __future__ import annotations

import json
import time
import uuid
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Deque, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


LONDON_TZ = ZoneInfo("Europe/London")
ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "watcher_config.json"
OBSERVATION_LOG = ROOT / "data" / "market_observations.jsonl"
EVENT_LOG = ROOT / "data" / "market_events.jsonl"


@dataclass
class PricePoint:
    timestamp: datetime
    price: float


def london_now() -> datetime:
    return datetime.now(LONDON_TZ)


def human_timestamp(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S %Z")


def iso_timestamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds")


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n")


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fetch_coinbase_spot_price(product: str, timeout_seconds: int) -> float:
    url = f"https://api.coinbase.com/v2/prices/{product}/spot"
    request = Request(
        url,
        headers={
            "User-Agent": "AI-Trading-Experiment-Watcher/0.1",
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=timeout_seconds) as response:
        payload = json.loads(response.read().decode("utf-8"))

    return float(payload["data"]["amount"])


def make_event_id(now: datetime) -> str:
    short_uuid = uuid.uuid4().hex[:8].upper()
    return f"EVT-{now.strftime('%Y%m%d-%H%M%S')}-{short_uuid}"


def percentage_change(old_price: float, new_price: float) -> float:
    return ((new_price - old_price) / old_price) * 100.0


def find_reference_point(
    history: Deque[PricePoint], now: datetime, lookback_seconds: int
) -> Optional[PricePoint]:
    target = now - timedelta(seconds=lookback_seconds)
    candidates = [point for point in history if point.timestamp <= target]
    return candidates[-1] if candidates else None


def prune_history(history: Deque[PricePoint], now: datetime, keep_seconds: int) -> None:
    cutoff = now - timedelta(seconds=keep_seconds)
    while history and history[0].timestamp < cutoff:
        history.popleft()


def main() -> None:
    config = load_config()

    product = config["product"]
    poll_seconds = int(config["poll_seconds"])
    lookback_seconds = int(config["lookback_seconds"])
    trigger_percent = float(config["trigger_percent"])
    cooldown_seconds = int(config["cooldown_seconds"])
    timeout_seconds = int(config["request_timeout_seconds"])
    test_mode = bool(config["test_mode"])

    history: Deque[PricePoint] = deque()
    last_event_time: Optional[datetime] = None

    started = london_now()
    print(
        f"[{human_timestamp(started)}] watcher started | product={product} "
        f"| test_mode={test_mode}"
    )

    while True:
        detected_at = london_now()

        try:
            price = fetch_coinbase_spot_price(product, timeout_seconds)
        except (HTTPError, URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as error:
            failure_time = london_now()
            failure_record = {
                "record_type": "WATCHER_ERROR",
                "timestamp_london": human_timestamp(failure_time),
                "timestamp_iso": iso_timestamp(failure_time),
                "product": product,
                "error_type": type(error).__name__,
                "error": str(error),
                "test_mode": test_mode,
            }
            append_jsonl(EVENT_LOG, failure_record)
            print(f"[{human_timestamp(failure_time)}] data fetch failed: {error}")
            time.sleep(poll_seconds)
            continue

        observed_at = london_now()
        history.append(PricePoint(timestamp=observed_at, price=price))
        prune_history(history, observed_at, max(lookback_seconds * 3, lookback_seconds + 60))

        observation = {
            "record_type": "PRICE_OBSERVATION",
            "market_id": "BTC-GBP",
            "product": product,
            "source": "Coinbase public spot endpoint",
            "watcher_detected_london": human_timestamp(detected_at),
            "watcher_detected_iso": iso_timestamp(detected_at),
            "observed_london": human_timestamp(observed_at),
            "observed_iso": iso_timestamp(observed_at),
            "price": price,
            "currency": "GBP",
            "test_mode": test_mode,
        }
        append_jsonl(OBSERVATION_LOG, observation)

        reference = find_reference_point(history, observed_at, lookback_seconds)
        if reference is not None:
            move_percent = percentage_change(reference.price, price)
            cooldown_clear = (
                last_event_time is None
                or (observed_at - last_event_time).total_seconds() >= cooldown_seconds
            )

            if abs(move_percent) >= trigger_percent and cooldown_clear:
                event_id = make_event_id(observed_at)
                direction = "UP" if move_percent > 0 else "DOWN"

                event = {
                    "record_type": "MARKET_EVENT",
                    "event_id": event_id,
                    "market_id": "BTC-GBP",
                    "product": product,
                    "source": "Coinbase public spot endpoint",
                    "event_type": "PRICE_MOVE",
                    "direction": direction,
                    "reference_price": reference.price,
                    "current_price": price,
                    "move_percent": round(move_percent, 6),
                    "lookback_seconds": lookback_seconds,
                    "trigger_percent": trigger_percent,
                    "event_occurred_london": human_timestamp(observed_at),
                    "event_occurred_iso": iso_timestamp(observed_at),
                    "watcher_detected_london": human_timestamp(observed_at),
                    "watcher_detected_iso": iso_timestamp(observed_at),
                    "ai_received_london": None,
                    "ai_decision_london": None,
                    "simulated_execution_london": None,
                    "test_mode": test_mode,
                    "status": "AWAITING_AI_REVIEW",
                }
                append_jsonl(EVENT_LOG, event)
                last_event_time = observed_at

                print(
                    f"[{human_timestamp(observed_at)}] {event_id} | "
                    f"{direction} {move_percent:.4f}% | £{reference.price:.2f} -> £{price:.2f}"
                )
            else:
                print(
                    f"[{human_timestamp(observed_at)}] BTC-GBP £{price:.2f} | "
                    f"move={move_percent:.4f}%"
                )
        else:
            print(
                f"[{human_timestamp(observed_at)}] BTC-GBP £{price:.2f} | "
                "building lookback history"
            )

        time.sleep(poll_seconds)


if __name__ == "__main__":
    main()
