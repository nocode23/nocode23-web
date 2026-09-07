#!/usr/bin/env python3
"""Publish committed website changes, children first. Dry run by default."""
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ('lacto-tracker', 'daily-routines-and-habits', 'limits')


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).rstrip('\n')


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true', help='Actually push committed changes and commit updated submodule pointers')
    args = parser.parse_args()
    subprocess.run(['python3', str(ROOT / 'scripts/verify.py')], check=True)
    require(git(ROOT, 'branch', '--show-current') == 'main', 'Main website must be on main.')
    require(not git(ROOT, 'diff', '--cached', '--name-only'), 'Commit or unstage the parent index first. No unrelated staged changes are allowed.')
    # The parent may only have changed submodule pointers, never uncommitted files.
    paths = git(ROOT, 'status', '--porcelain', '--untracked-files=all').splitlines()
    allowed = {f'www/{name}' for name in MODULES}
    require(all(line[3:] in allowed for line in paths), 'Commit all parent website files before publishing.')
    repos = [ROOT / 'www' / name for name in MODULES]
    for repo in repos:
        require(git(repo, 'branch', '--show-current') == 'main', f'{repo.name}: switch to main before publishing.')
        require(not git(repo, 'status', '--porcelain'), f'{repo.name}: commit changes before publishing.')
        # Unknown active hooks must be reviewed; do not silently bypass them.
        hook_path = Path(git(repo, 'rev-parse', '--git-path', 'hooks/pre-push'))
        if not hook_path.is_absolute():
            hook_path = repo / hook_path
        require(not hook_path.exists(), f'{repo.name}: review/remove the old pre-push hook with scripts/retire-legacy-hook.py first.')
    print('Order: ' + ' → '.join([r.name for r in repos] + ['nocode23-web']))
    if not args.publish:
        print('Dry run passed. Run with --publish only when ready to deploy via Cloudflare Pages.')
        return
    for repo in repos:
        subprocess.run(['git', '-C', str(repo), 'push', 'origin', 'HEAD:refs/heads/main'], check=True)
        remote = git(repo, 'ls-remote', '--exit-code', 'origin', 'refs/heads/main').split()[0]
        require(remote == git(repo, 'rev-parse', 'HEAD'), f'{repo.name}: remote changed; stopped before updating the parent.')
    subprocess.run(['git', '-C', str(ROOT), 'add', '--', *sorted(allowed)], check=True)
    if git(ROOT, 'diff', '--cached', '--name-only'):
        subprocess.run(['git', '-C', str(ROOT), 'commit', '-m', '[www] update published project references'], check=True)
    subprocess.run(['git', '-C', str(ROOT), 'push', 'origin', 'HEAD:refs/heads/main'], check=True)
    print('GitHub updated. Check Cloudflare Pages deployment before treating the site as live.')


if __name__ == '__main__':
    main()
