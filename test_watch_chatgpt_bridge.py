from datetime import datetime, timedelta
import json
from pathlib import Path
import tempfile
import unittest

from chatgpt_bridge import Ledger, LONDON
from watch_chatgpt_bridge import NewLines, eligible, follow, follower_lock

NOW = datetime(2026, 9, 15, 22, 0, tzinfo=LONDON)


def event(name='fresh', at=NOW):
    return dict(record_type='MARKET_EVENT', event_id=name, product='BTC-GBP',
                test_mode=True, watcher_detected_iso=at.isoformat())


def row(value):
    return (json.dumps(value) + '\n').encode()


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / 'events.jsonl'
        self.path.write_bytes(row(event('old')))
        self.ledger = Ledger(self.root / 'ledger.sqlite3')
    def tearDown(self):
        self.ledger.db.close()
        self.temp.cleanup()
    def append(self, data):
        with self.path.open('ab') as out:
            out.write(data)
    def test_no_backlog_and_restart_no_replay(self):
        reader = NewLines(self.path)
        self.assertEqual(reader.poll(), [])
        self.append(row(event()))
        self.assertEqual([json.loads(x)['event_id'] for x in reader.poll()], ['fresh'])
        self.assertEqual(NewLines(self.path).poll(), [])
    def test_wait_for_complete_new_line(self):
        reader = NewLines(self.path)
        value = row(event())
        self.append(value[:20])
        self.assertEqual(reader.poll(), [])
        self.append(value[20:])
        self.assertEqual(len(reader.poll()), 1)
    def test_skip_initial_partial_line(self):
        value = row(event('old-partial'))
        self.append(value[:20])
        reader = NewLines(self.path)
        self.append(value[20:] + row(event()))
        self.assertEqual([json.loads(x)['event_id'] for x in reader.poll()], ['fresh'])
    def test_rewrite_and_truncation_stop(self):
        for value in [b'', b'x' * len(self.path.read_bytes())]:
            reader = NewLines(self.path)
            self.path.write_bytes(value)
            with self.assertRaises(RuntimeError):
                reader.poll()
            self.path.write_bytes(row(event('old')))
    def test_replacement_stops(self):
        reader = NewLines(self.path)
        other = self.root / 'replacement'
        other.write_bytes(self.path.read_bytes())
        other.replace(self.path)
        with self.assertRaises(RuntimeError):
            reader.poll()
    def test_freshness_and_prelaunch(self):
        self.assertIsNone(eligible(event(), NOW, NOW))
        self.assertEqual(eligible(event(at=NOW-timedelta(seconds=1)), NOW, NOW), 'PREDATES_ARMING')
        self.assertEqual(eligible(event(), NOW, NOW+timedelta(seconds=61)), 'STALE_EVENT')
        self.assertEqual(eligible(event(at=NOW+timedelta(seconds=1)), NOW, NOW), 'FUTURE_TIMESTAMP')
        with self.assertRaises(ValueError):
            eligible(dict(event(), test_mode=False), NOW, NOW)
    def test_one_send_only(self):
        elapsed = [0]
        sends = []
        def sleep(seconds):
            elapsed[0] += seconds
            self.append(row(event('one')) + row(event('two')))
        def send(value, target, ledger):
            sends.append(value['event_id'])
            return 'CHATGPT SUBMITTED'
        result = follow(self.path, self.ledger, sender=send, clock=lambda: NOW,
                        monotonic=lambda: elapsed[0], sleep=sleep)
        self.assertEqual(result, 'ONE_MESSAGE_SUBMITTED')
        self.assertEqual(sends, ['one'])
    def test_failure_stops_and_does_not_send_next(self):
        elapsed = [0]
        calls = []
        def sleep(seconds):
            elapsed[0] += seconds
            self.append(row(event('one')) + row(event('two')))
        def send(value, target, ledger):
            calls.append(value['event_id'])
            raise TimeoutError('uncertain')
        with self.assertRaises(TimeoutError):
            follow(self.path, self.ledger, sender=send, clock=lambda: NOW,
                   monotonic=lambda: elapsed[0], sleep=sleep)
        self.assertEqual(calls, ['one'])
        kinds = [json.loads(x[0])['record_type'] for x in self.ledger.db.execute('SELECT record FROM audit')]
        self.assertIn('FOLLOWER ERROR', kinds)
    def test_timeout_and_source_preservation(self):
        elapsed = [0]
        before = self.path.read_bytes()
        def sleep(seconds):
            elapsed[0] += seconds
        def send(*args):
            self.fail('No old event may be submitted')
        result = follow(self.path, self.ledger, seconds=1, sender=send, clock=lambda: NOW,
                        monotonic=lambda: elapsed[0], sleep=sleep)
        self.assertEqual(result, 'TIMEOUT_NO_SUBMISSION')
        self.assertEqual(before, self.path.read_bytes())
    def test_no_second_follower(self):
        with follower_lock(self.ledger):
            with self.assertRaises(FileExistsError):
                follow(self.path, self.ledger)


if __name__ == '__main__':
    unittest.main()
