import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checklist', ROOT / 'skills/job-checklists/scripts/checklist.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
spec_install = importlib.util.spec_from_file_location('installer', ROOT / 'install.py')
installer = importlib.util.module_from_spec(spec_install)
spec_install.loader.exec_module(installer)


class ChecklistTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.data = self.base / 'private'
        self.template = self.base / 'template.json'
        self.template.write_text(json.dumps({'version': '1', 'tasks': [{'id': 'check', 'text': 'Check approved scope'}]}))

    def new(self, key='job-1'):
        return helper.create(self.data, key, 'Synthetic job', self.template, 'test owner')

    def test_fresh_instances_and_history(self):
        self.new()
        helper.update(self.data, 'job-1', 'check', 'done', 'test assignee')
        reopened = helper.update(self.data, 'job-1', 'check', 'open', 'test owner', 'Recheck')
        self.assertEqual([x.get('state') for x in reopened['events']], [None, 'done', 'open'])
        second = self.new('job-2')
        self.assertEqual(len(second['events']), 1)
        self.assertIn('[ ]', helper.render(second))
        self.assertEqual(len(helper.read_json(self.data / 'job-1.json')['events']), 3)

    def test_blocker_reason_and_attribution_visible(self):
        self.new()
        record = helper.update(self.data, 'job-1', 'check', 'blocked', 'test worker', 'Waiting for approved scope')
        shown = helper.render(record)
        self.assertIn('Waiting for approved scope', shown)
        self.assertIn('test worker', shown)
        self.assertIn(record['events'][-1]['at'], shown)

    def test_duplicate_trigger_preserves_completed_state(self):
        self.new()
        helper.update(self.data, 'job-1', 'check', 'done', 'test assignee')
        replay = self.new()
        self.assertEqual(len(replay['events']), 2)
        self.assertIn('[x]', helper.render(replay))

    def test_template_snapshot_and_conflicting_key(self):
        self.new()
        self.template.write_text(json.dumps({'version': '2', 'tasks': [{'id': 'other', 'text': 'Different'}]}))
        with self.assertRaises(ValueError):
            self.new()
        self.assertEqual(helper.read_json(self.data / 'job-1.json')['template']['version'], '1')

    def test_reject_invalid_updates_and_path_traversal(self):
        self.new()
        before = (self.data / 'job-1.json').read_bytes()
        for task, state in [('missing', 'done'), ('check', 'invented')]:
            with self.assertRaises(ValueError):
                helper.update(self.data, 'job-1', task, state, 'test')
        with self.assertRaises(ValueError):
            self.new('../escape')
        self.assertEqual(before, (self.data / 'job-1.json').read_bytes())

    def test_single_writer_lock(self):
        self.new()
        (self.data / '.lock').write_text('test')
        with self.assertRaises(ValueError):
            helper.update(self.data, 'job-1', 'check', 'done', 'test')
        self.assertTrue((self.data / '.lock').exists())

    def test_duplicate_task_ids_rejected(self):
        self.template.write_text(json.dumps({'version': '1', 'tasks': [{'id': 'x', 'text': 'A'}, {'id': 'x', 'text': 'B'}]}))
        with self.assertRaises(ValueError):
            self.new()

    def test_install_and_refuse_overwrite(self):
        target = installer.install(self.base / 'skills')
        self.assertTrue((target / 'SKILL.md').is_file())
        self.assertFalse(list(target.rglob('__pycache__')))
        self.assertFalse(list(target.rglob('*.pyc')))
        (target / 'private-note').write_text('preserve')
        with self.assertRaises(ValueError):
            installer.install(self.base / 'skills')
        self.assertEqual((target / 'private-note').read_text(), 'preserve')


if __name__ == '__main__':
    unittest.main()
