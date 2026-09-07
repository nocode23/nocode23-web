#!/usr/bin/env python3
"""Archive only the known unsafe local Daily Routines hook; never execute it."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
repo = root / 'www/daily-routines-and-habits'
path = Path(subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--git-path', 'hooks/pre-push'], text=True).strip())
if not path.is_absolute():
    path = repo / path
expected = '''#!/bin/sh
# After pushing daily-routines-and-habits, update submodule reference in main repo

MAIN_REPO="$(git rev-parse --show-toplevel)/../.."

cd "$MAIN_REPO" || exit 1

git add www/daily-routines-and-habits
git commit -m "[www] update daily-routines-and-habits submodule reference"
git push origin main
'''
if not path.exists():
    print('No legacy pre-push hook is installed.')
elif path.read_text() != expected:
    raise SystemExit('Hook differs from the audited version; left untouched.')
else:
    backup = path.with_name('pre-push.legacy-disabled')
    if backup.exists():
        raise SystemExit('Backup already exists; left both files untouched.')
    path.rename(backup)
    print('Unsafe hook archived as pre-push.legacy-disabled. Use scripts/publish.py for releases.')
