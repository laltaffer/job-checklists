"""Copy the reviewed skill into a local discovery directory without replacing data."""
import argparse
import shutil
from pathlib import Path


def install(destination):
    source = Path(__file__).resolve().parent / 'skills' / 'job-checklists'
    target = Path(destination).expanduser().resolve() / 'job-checklists'
    if target.exists():
        raise ValueError(f'Installation already exists: {target}; nothing changed')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', default=str(Path.home() / '.agents' / 'skills'))
    args = parser.parse_args()
    try:
        print(f'Installed: {install(args.destination)}')
    except ValueError as exc:
        parser.exit(1, f'{exc}\n')
