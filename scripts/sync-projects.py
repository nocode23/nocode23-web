#!/usr/bin/env python3
"""Generate the portfolio's project summaries and counts; HTML works without JS."""
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generated(source):
    projects = json.loads((ROOT / 'www/data/apps.json').read_text())['projects']
    for project in projects:
        key = project['id']
        external = project['url'].startswith('https://')
        attrs = ' target="_blank" rel="noopener"' if external else ''
        esc = lambda key: html.escape(project[key], quote=True)
        block = f'''<!-- project:{key}:start -->
              <a href="{esc('url')}" class="feat-project" data-project="{key}"{attrs}>
                <img src="{esc('logo')}" alt="" class="feat-logo" loading="lazy" width="36" height="36">
                <div class="feat-info">
                  <div class="feat-name">{esc('name')}</div>
                  <div class="feat-sub">{esc('description')}</div>
                </div>
                <span class="feat-arrow" aria-hidden="true">{'↗' if external else '→'}</span>
              </a>
              <p class="project-note">{esc('note')}</p>
<!-- project:{key}:end -->'''
        source, count = re.subn(r'<!-- project:' + re.escape(key) + r':start -->[\s\S]*?<!-- project:' + re.escape(key) + r':end -->', lambda _: block, source)
        if count != 1:
            raise SystemExit(f'Expected exactly one project marker for {key}, found {count}')
    for name, value in [('projects', len(projects)), ('apps', sum(p['type'] == 'app' for p in projects))]:
        source, count = re.subn(r'(<div class="stat-num" data-stat="' + name + r'">)\d+(</div>)', lambda m: m[1] + str(value) + m[2], source)
        if count != 1:
            raise SystemExit(f'Missing statistic: {name}')
    return source


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'www/index.html'
    before = path.read_text()
    after = generated(before)
    if args.check:
        if before != after:
            raise SystemExit('Project data and homepage differ. Run python3 scripts/sync-projects.py')
        print('Project metadata and counts match.')
    else:
        path.write_text(after)
        print('Project summaries and counts updated.')
