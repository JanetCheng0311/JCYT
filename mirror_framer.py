#!/usr/bin/env python3
import os
import sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

BASE = 'https://jcyt.framer.website'
ROOT = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(ROOT, 'assets', 'download')
os.makedirs(ASSETS_DIR, exist_ok=True)

def save_url(url, path):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print('Failed to fetch', url, e)
        return None
    with open(path, 'wb') as f:
        f.write(r.content)
    return path

def asset_local_path(asset_url):
    parsed = urlparse(asset_url)
    filename = os.path.basename(parsed.path) or 'asset'
    local = os.path.join(ASSETS_DIR, filename)
    return local, os.path.relpath(local, ROOT).replace('\\\\','/')

def normalize_page_path(path):
    if path in ('', '/'):
        return 'index.html'
    if path.startswith('/'):
        path = path[1:]
    if path.endswith('/'):
        path = path + 'index.html'
    if not path.lower().endswith('.html'):
        path = path + '.html'
    return path

visited = set()
to_visit = ['/']

while to_visit:
    path = to_visit.pop(0)
    if path in visited:
        continue
    visited.add(path)
    full = urljoin(BASE, path)
    print('Crawling', full)
    try:
        resp = requests.get(full, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print('Failed', full, e)
        continue
    soup = BeautifulSoup(resp.text, 'html.parser')

    # find internal links
    for a in soup.find_all('a', href=True):
        href = a['href']
        parsed = urlparse(href)
        if parsed.netloc == '' or parsed.netloc.endswith('framer.website'):
            # internal
            p = parsed.path or '/'
            if p not in visited and p not in to_visit:
                to_visit.append(p)

    # download assets (img, script, link rel=stylesheet)
    for tag, attr in (('img','src'), ('script','src'), ('link','href')):
        for t in soup.find_all(tag):
            if not t.has_attr(attr):
                continue
            src = t[attr]
            parsed = urlparse(src)
            if parsed.scheme and not parsed.netloc.endswith('framer.website') and parsed.netloc != '':
                # external - skip
                continue
            asset_url = urljoin(full, src)
            local_path, rel = asset_local_path(asset_url)
            if not os.path.exists(local_path):
                saved = save_url(asset_url, local_path)
                if saved:
                    print('Saved asset', asset_url, '->', local_path)
            # update tag to point to local relative path
            t[attr] = '/' + rel

    # write modified HTML
    outpath = os.path.join(ROOT, normalize_page_path(urlparse(path).path))
    outdir = os.path.dirname(outpath)
    os.makedirs(outdir, exist_ok=True)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print('Wrote', outpath)

print('Crawl complete. Pages saved under', ROOT)
