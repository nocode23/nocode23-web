"""Release ordering and failure isolation against disposable local Git remotes."""
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('publish', Path(__file__).resolve().parents[1] / 'scripts/publish.py')
publish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publish)
RUN = subprocess.run


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'site'
        self.env = patch.dict(os.environ, {'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.root.mkdir()
        self.init_repo(self.root, 'site')
        self.children = []
        for name in publish.MODULES:
            repo = self.root / 'www' / name
            repo.mkdir(parents=True)
            self.init_repo(repo, name)
            self.children.append(repo)
        self.git(self.root, 'add', '.')
        self.git(self.root, 'commit', '-qm', 'Initial submodule pointers')
        self.git(self.root, 'push', '-q', 'origin', 'main')
        self.initial_parent = self.git(self.root, 'rev-parse', 'HEAD')
        for repo in self.children:
            (repo / 'index.html').write_text('Updated site')
            self.git(repo, 'add', 'index.html')
            self.git(repo, 'commit', '-qm', 'Update site')

    def git(self, repo, *args):
        return subprocess.check_output(['git', '-C', str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()

    def init_repo(self, repo, name):
        remote = self.base / (name + '.git')
        RUN(['git', 'init', '--bare', '-q', str(remote)], check=True)
        self.git(repo, 'init', '-q', '-b', 'main')
        self.git(repo, 'config', 'user.name', 'Release test')
        self.git(repo, 'config', 'user.email', 'test@example.invalid')
        self.git(repo, 'remote', 'add', 'origin', str(remote))
        (repo / 'index.html').write_text('Initial site')
        self.git(repo, 'add', '.')
        self.git(repo, 'commit', '-qm', 'Initial site')
        self.git(repo, 'push', '-q', 'origin', 'main')

    def remote_head(self, name):
        return self.git(self.base / (name + '.git'), 'rev-parse', 'refs/heads/main')

    def invoke(self, publish_changes=True):
        self.events = []

        def run(command, **kwargs):
            # HTML validation has its own real invocation outside these Git-only fixtures.
            if command[:1] == ['python3']:
                return subprocess.CompletedProcess(command, 0)
            if 'push' in command:
                self.events.append(Path(command[2]).name)
            return RUN(command, **kwargs)

        with patch.object(publish, 'ROOT', self.root), patch.object(publish.subprocess, 'run', side_effect=run), patch('sys.argv', ['publish.py'] + (['--publish'] if publish_changes else [])):
            publish.main()

    def test_children_are_published_before_parent(self):
        self.invoke()
        self.assertEqual(self.events, [*publish.MODULES, 'site'])
        for repo in self.children:
            head = self.git(repo, 'rev-parse', 'HEAD')
            self.assertEqual(self.remote_head(repo.name), head)
            self.assertEqual(self.git(self.root, 'rev-parse', f'HEAD:www/{repo.name}'), head)
        self.assertEqual(self.remote_head('site'), self.git(self.root, 'rev-parse', 'HEAD'))

    def test_failed_child_push_never_publishes_parent(self):
        remote = self.base / (publish.MODULES[1] + '.git')
        hook = remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        with self.assertRaises(subprocess.CalledProcessError):
            self.invoke()
        self.assertEqual(self.remote_head('site'), self.initial_parent)
        self.assertEqual(self.git(self.root, 'rev-parse', 'HEAD'), self.initial_parent)
        self.assertEqual(self.git(self.root, 'diff', '--cached', '--name-only'), '')

    def test_unrelated_staged_changes_are_not_committed(self):
        (self.root / 'unrelated.txt').write_text('Work in progress')
        self.git(self.root, 'add', 'unrelated.txt')
        with self.assertRaisesRegex(SystemExit, 'parent index'):
            self.invoke()
        self.assertEqual(self.events, [])
        self.assertEqual(self.git(self.root, 'diff', '--cached', '--name-only'), 'unrelated.txt')

    def test_dry_run_does_not_push_or_commit(self):
        self.invoke(False)
        self.assertEqual(self.events, [])
        self.assertEqual(self.git(self.root, 'rev-parse', 'HEAD'), self.initial_parent)

    def test_legacy_hook_blocks_release(self):
        hook = self.children[0] / '.git/hooks/pre-push'
        hook.write_text('#!/bin/sh\nexit 0\n')
        with self.assertRaisesRegex(SystemExit, 'pre-push hook'):
            self.invoke()
        self.assertEqual(self.events, [])


if __name__ == '__main__':
    unittest.main()
