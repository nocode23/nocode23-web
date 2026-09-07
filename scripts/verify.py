#!/usr/bin/env python3
"""Dependency-free checks of public HTML, links, downloads, metadata and project data."""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT / 'www'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.refs = []
        self.canonicals = []
        self.alternates = []
        self.noindex = False
        self.title = False
        self.issues = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.issues.append(f'duplicate id: {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'title':
            self.title = True
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.noindex = 'noindex' in attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'link' and attrs.get('rel') == 'alternate' and 'hreflang' in attrs:
            self.alternates.append(attrs.get('href', ''))
        for key in ('href', 'src'):
            if attrs.get(key):
                self.refs.append(attrs[key])
        if attrs.get('srcset'):
            self.refs.extend(part.strip().split()[0] for part in attrs['srcset'].split(','))
        if tag == 'a' and any(c in attrs.get('class', '').split() for c in ('dl-btn', 'appstore-badge', 'btn-nav-download')):
            if not attrs.get('href', '').startswith('https://apps.apple.com/'):
                self.issues.append('download CTA does not point to App Store')


def main():
    pages = {p.resolve(): Page(p) for p in WWW.rglob('*.html') if 'tools' not in p.relative_to(WWW).parts}
    issues = []
    for path, page in pages.items():
        for issue in page.issues:
            issues.append(f'{page.path}: {issue}')
        if not page.title:
            issues.append(f'{page.path}: missing title')
        if not page.noindex and (len(page.canonicals) != 1 or not page.canonicals[0].startswith('https://nocode23.com/')):
            issues.append(f'{page.path}: expected one absolute canonical')
        for ref in page.alternates:
            if not ref.startswith('https://nocode23.com/'):
                issues.append(f'{page.path}: non-absolute hreflang: {ref}')
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                if url.netloc != 'nocode23.com':
                    continue
                target = WWW / unquote(url.path.lstrip('/'))
            elif url.path:
                target = WWW / unquote(url.path.lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
            else:
                target = path
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            if not target.is_relative_to(WWW.resolve()) or not target.exists():
                issues.append(f'{page.path}: missing local target {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                issues.append(f'{page.path}: missing anchor {ref}')
    sitemap = ET.parse(WWW / 'sitemap.xml')
    urls = {el.text for el in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
    for page in pages.values():
        if not page.noindex and page.canonicals and page.canonicals[0] not in urls:
            issues.append(f'{page.path}: canonical missing from sitemap')
    data = json.loads((WWW / 'data/apps.json').read_text())['projects']
    if len({p['id'] for p in data}) != len(data):
        issues.append('Duplicate project IDs')
    check = subprocess.run([sys.executable, str(ROOT / 'scripts/sync-projects.py'), '--check'])
    if check.returncode:
        issues.append('Generated project metadata is stale')
    if issues:
        raise SystemExit('\n'.join(issues))
    print(f'PASS: {len(pages)} HTML pages, local assets/anchors, download links, sitemap, canonical/hreflang and {len(data)} projects.')


if __name__ == '__main__':
    main()
