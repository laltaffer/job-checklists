"""Local single-writer checklist ledger. No sharing, scheduling or verified identity."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile

STATES = {'open', 'done', 'blocked', 'not_applicable'}


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', value):
        raise ValueError('IDs must use 1–80 letters, numbers, underscores or hyphens')
    return value


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def template_data(path):
    value = read_json(path)
    if not isinstance(value, dict) or not isinstance(value.get('version'), str) or not value['version']:
        raise ValueError('Template needs a nonempty string version')
    tasks = value.get('tasks')
    if not isinstance(tasks, list) or not tasks:
        raise ValueError('Template needs at least one task')
    clean = []
    seen = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError('Each task must be an object')
        key = identifier(task.get('id'))
        if key in seen or not isinstance(task.get('text'), str) or not task['text'].strip():
            raise ValueError('Tasks need unique IDs and nonempty text')
        seen.add(key)
        clean.append({'id': key, 'text': task['text']})
    return {'version': value['version'], 'tasks': clean}


@contextmanager
def locked(directory):
    directory = Path(directory).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = directory / '.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError('Data directory locked. Confirm no writer is running before removing a stale .lock')
    try:
        os.close(fd)
        yield directory
    finally:
        lock.unlink()


def write_json(path, value):
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.pending-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            json.dump(value, output, ensure_ascii=False, indent=2)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def event(kind, actor, **fields):
    if not actor.strip():
        raise ValueError('Actor label cannot be empty')
    return {'kind': kind, 'actor': actor, 'at': datetime.now(timezone.utc).isoformat(), **fields}


def create(directory, job_id, title, template_path, actor):
    identifier(job_id)
    if not title.strip():
        raise ValueError('Title cannot be empty')
    template = template_data(template_path)
    with locked(directory) as root:
        path = root / f'{job_id}.json'
        if path.exists():
            previous = read_json(path)
            if previous['template'] != template or previous['title'] != title:
                raise ValueError('Job key already exists with different inputs; use a new key or review the existing record')
            return previous
        record = {'id': job_id, 'title': title, 'template': template,
                  'events': [event('created', actor)]}
        write_json(path, record)
        return record


def update(directory, job_id, task_id, state, actor, note=''):
    identifier(job_id)
    if state not in STATES:
        raise ValueError('Unsupported state')
    with locked(directory) as root:
        path = root / f'{job_id}.json'
        record = read_json(path)
        if task_id not in {task['id'] for task in record['template']['tasks']}:
            raise ValueError('Unknown task ID')
        record['events'].append(event('state', actor, task_id=task_id, state=state, note=note))
        write_json(path, record)
        return record


def render(record):
    current = {task['id']: 'open' for task in record['template']['tasks']}
    for entry in record['events']:
        if entry['kind'] == 'state':
            current[entry['task_id']] = entry['state']
    lines = [f"# {record['title']}", f"Job: {record['id']} · Template: {record['template']['version']}",
             'Local record; actor labels are self-reported.', '']
    for task in record['template']['tasks']:
        state = current[task['id']]
        marker = 'x' if state == 'done' else ' '
        lines.append(f"- [{marker}] {task['text']} ({task['id']}: {state})")
    lines.extend(['', '## Recorded activity'])
    for entry in record['events']:
        detail = 'Created' if entry['kind'] == 'created' else f"{entry['task_id']} → {entry['state']}"
        lines.append(f"- {entry['at']} · {entry['actor']}: {detail}")
        if entry.get('note'):
            lines.append(f"  Note: {entry['note']}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True, help='Private state directory outside the installed skill/public repository')
    commands = parser.add_subparsers(dest='command', required=True)
    new = commands.add_parser('create', help='Create a fresh instance or return the identical existing instance')
    new.add_argument('--job', required=True)
    new.add_argument('--title', required=True)
    new.add_argument('--template', required=True)
    new.add_argument('--actor', required=True)
    change = commands.add_parser('update', help='Append a task state change')
    change.add_argument('--job', required=True)
    change.add_argument('--task', required=True)
    change.add_argument('--state', choices=sorted(STATES), required=True)
    change.add_argument('--actor', required=True)
    change.add_argument('--note', default='')
    show = commands.add_parser('show', help='Render current state; editing the output does not change the ledger')
    show.add_argument('--job', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'create':
            record = create(args.data_dir, args.job, args.title, args.template, args.actor)
        elif args.command == 'update':
            record = update(args.data_dir, args.job, args.task, args.state, args.actor, args.note)
        else:
            identifier(args.job)
            record = read_json(Path(args.data_dir).expanduser().resolve() / f'{args.job}.json')
        print(render(record))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'Checklist error: {exc}\n')


if __name__ == '__main__':
    main()
