import json
from pathlib import Path
import tempfile
import unittest
from datetime import datetime
from chatgpt_bridge import Browser, Ledger, exclusive_browser, stamp, submit, target_key, validate
from unittest.mock import MagicMock

URL = "https://chatgpt.com/c/test-conversation"
EVENT = dict(record_type="MARKET_EVENT", event_id="TEST-001", product="BTC-GBP",
             test_mode=True, watcher_detected_iso="2026-09-15T20:00:00+01:00")


class FakeBrowser:
    sends = 0
    fail = False
    def prepare(self, url):
        pass
    def send(self, message):
        assert '\n' not in message
        FakeBrowser.sends += 1
        if FakeBrowser.fail:
            raise TimeoutError("Uncertain after Enter")
    def close(self):
        pass


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "ledger.sqlite3"
        self.ledger = Ledger(self.path)
        FakeBrowser.sends = 0
        FakeBrowser.fail = False
    def tearDown(self):
        self.ledger.db.close()
        self.temp.cleanup()
    def test_restart_duplicate(self):
        submit(EVENT, URL, self.ledger, FakeBrowser)
        self.ledger.db.close()
        self.ledger = Ledger(self.path)
        submit(EVENT, URL, self.ledger, FakeBrowser)
        self.assertEqual(FakeBrowser.sends, 1)
        records = [json.loads(r[0]) for r in self.ledger.db.execute("SELECT record FROM audit")]
        self.assertIn("CHATGPT SUBMITTED", [r['record_type'] for r in records])
        self.assertTrue(all(r['timezone'] == 'Europe/London' for r in records))
    def test_uncertain_send_never_retried(self):
        FakeBrowser.fail = True
        with self.assertRaises(TimeoutError):
            submit(EVENT, URL, self.ledger, FakeBrowser)
        submit(EVENT, URL, self.ledger, FakeBrowser)
        self.assertEqual(FakeBrowser.sends, 1)
        rows = [json.loads(r[0])['record_type'] for r in self.ledger.db.execute('SELECT record FROM audit')]
        self.assertNotIn('CHATGPT SUBMITTED', rows)
    def test_id_collision(self):
        submit(EVENT, URL, self.ledger, FakeBrowser)
        with self.assertRaises(ValueError):
            submit(dict(EVENT, reason='changed'), URL, self.ledger, FakeBrowser)
        self.assertEqual(FakeBrowser.sends, 1)
    def test_crash_after_claim(self):
        self.assertTrue(self.ledger.claim('x', 'hash', URL))
        other = Ledger(self.path)
        try:
            self.assertFalse(other.claim('x', 'hash', URL))
        finally:
            other.db.close()
    def test_prelaunch_only(self):
        for update in [dict(test_mode=False), dict(product='ETH-GBP'), dict(watcher_detected_iso='2026-09-15T20:00:00')]:
            with self.assertRaises(ValueError):
                validate(dict(EVENT, **update))
    def test_target_validation(self):
        for url in ['https://chatgpt.com/', 'http://chatgpt.com/c/x', 'https://chatgpt.com.evil/c/x', URL+'?x=1']:
            with self.assertRaises(ValueError):
                target_key(url)
        self.assertEqual(target_key('https://chatgpt.com/g/project/c/abc'), '/g/project/c/abc')
    def test_dst(self):
        for date, zone, offset in [('2026-01-15T12:00:00+00:00', 'GMT', '+00:00'), ('2026-07-15T12:00:00+00:00', 'BST', '+01:00')]:
            result = stamp(datetime.fromisoformat(date))
            self.assertTrue(result['timestamp_london'].endswith(zone))
            self.assertTrue(result['timestamp_iso'].endswith(offset))
    def test_concurrent_browser_blocked(self):
        with exclusive_browser(self.ledger):
            with self.assertRaises(FileExistsError):
                submit(EVENT, URL, self.ledger, FakeBrowser)
        self.assertEqual(FakeBrowser.sends, 0)
    def test_wrong_or_duplicate_tab(self):
        for handles, url in [(['a'], 'https://chatgpt.com/'), (['a', 'b'], URL)]:
            browser = Browser.__new__(Browser)
            browser.driver = MagicMock()
            browser.driver.window_handles = handles
            browser.driver.current_url = url
            with self.assertRaises(RuntimeError):
                browser.prepare(URL)
    def test_draft_preserved(self):
        browser = Browser.__new__(Browser)
        browser.driver = MagicMock()
        browser.driver.window_handles = ['a']
        browser.driver.current_url = URL
        box = MagicMock()
        box.get_attribute.return_value = 'existing draft'
        browser.driver.find_elements.side_effect = [[box], []]
        with self.assertRaises(RuntimeError):
            browser.prepare(URL)
        box.send_keys.assert_not_called()


if __name__ == '__main__':
    unittest.main()
