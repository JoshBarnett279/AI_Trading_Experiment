import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from bridge import MESSAGE, LONDON, append, collect, records


class BridgeTests(unittest.TestCase):
    def test_filter_deduplicate_restart_and_preserve_source(self):
        with tempfile.TemporaryDirectory() as root:
            events, outbox = Path(root) / "events", Path(root) / "outbox"
            good = dict(record_type="MARKET_EVENT", event_id="TEST-001",
                        product="BTC-GBP", test_mode=True)
            for item in [good, good, dict(good, event_id="LIVE", test_mode=False),
                         dict(good, event_id="ERROR", record_type="WATCHER_ERROR")]:
                append(events, item)
            before = events.read_bytes()
            self.assertEqual(collect(events, outbox), 1)
            saved = outbox.read_bytes()
            self.assertEqual(collect(events, outbox), 0)
            self.assertEqual(outbox.read_bytes(), saved)
            self.assertEqual(events.read_bytes(), before)
            self.assertEqual(records(outbox)[0]["message"], MESSAGE)

    def test_partial_event_waits_for_newline(self):
        with tempfile.TemporaryDirectory() as root:
            events, outbox = Path(root) / "events", Path(root) / "outbox"
            events.write_text(json.dumps(dict(record_type="MARKET_EVENT",
                event_id="TEST-PARTIAL", product="BTC-GBP", test_mode=True)))
            self.assertEqual(collect(events, outbox), 0)
            with events.open("a") as stream:
                stream.write("\n")
            self.assertEqual(collect(events, outbox), 1)
            with outbox.open("ab") as stream:
                stream.write(b'{')
            with self.assertRaises(ValueError):
                collect(events, outbox)

    def test_london_daylight_saving(self):
        self.assertEqual(datetime(2026, 1, 1, tzinfo=LONDON).tzname(), "GMT")
        self.assertEqual(datetime(2026, 7, 1, tzinfo=LONDON).tzname(), "BST")


if __name__ == "__main__":
    unittest.main()
