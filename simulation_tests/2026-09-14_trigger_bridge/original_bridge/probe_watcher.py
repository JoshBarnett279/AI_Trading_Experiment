"""Run the watcher's actual event branch with synthetic prices in isolation."""
import importlib.util
import json
import sys
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch
from bridge import append, collect, LONDON
from datetime import datetime

source = Path('C:/Users/LocalAdmin/OneDrive/Documents/GitHub/AI_Trading_Experiment/watcher/market_watcher.py')
spec = importlib.util.spec_from_file_location('watcher_probe', source)
watcher = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = watcher
spec.loader.exec_module(watcher)
root = Path(__file__).resolve().parent / 'test_evidence'
now = datetime.now(LONDON)
run = root / now.strftime('%Y%m%d-%H%M%S-%f')
events, outbox = run / 'synthetic_market_events.jsonl', run / 'outbox.jsonl'
config = watcher.load_config()
assert config['test_mode'] is True
start = now - timedelta(seconds=301)

class Done(Exception):
    pass

with patch.object(watcher, 'OBSERVATION_LOG', run / 'synthetic_observations.jsonl'), \
     patch.object(watcher, 'EVENT_LOG', events), \
     patch.object(watcher, 'london_now', side_effect=[start, start, start, now, now]), \
     patch.object(watcher, 'fetch_coinbase_spot_price', side_effect=[60000.0, 60600.0]), \
     patch.object(watcher.time, 'sleep', side_effect=[None, Done()]):
    try:
        watcher.main()
    except Done:
        pass
assert collect(events, outbox) == 1
original = outbox.read_bytes()
assert collect(events, outbox) == 0
assert original == outbox.read_bytes()
stamp = datetime.now(LONDON)
append(root / 'audit.jsonl', {
    'record_type': 'BRIDGE_LOCAL_TEST_PASSED',
    'timestamp_london': stamp.strftime('%Y-%m-%d %H:%M:%S %Z'),
    'timestamp_iso': stamp.isoformat(timespec='seconds'),
    'timezone': 'Europe/London', 'test_mode': True,
    'evidence_directory': str(run), 'synthetic_prices': True,
    'synthetic_observation_times': True,
    'watcher_event_branch_tested': True, 'desktop_delivery_tested': False,
    'clock_started': False, 'trades_executed': False,
})
print(json.dumps({'local_test': 'PASSED', 'desktop_delivery': 'NOT_CONNECTED',
                  'evidence': str(run)}))
