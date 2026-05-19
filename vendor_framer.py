import os
import re
import html
from urllib.parse import urlparse
import requests

ROOT = os.path.abspath(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, 'assets', 'vendor', 'framer')
os.makedirs(OUT_DIR, exist_ok=True)

DOMAINS = [
    r'framerusercontent\.com',
    r'framer\.com',
    r'events\.framer\.com',
    r'fonts\.gstatic\.com',
    r'fonts\.googleapis\.com',
]
PATTERN = re.compile(
    r'(?P<prefix>\bhttps?:)?//?(?P<host>'
    + r'|'.join(DOMAINS)
    + r')(?P<path>/[^"\'\s>\)]+)'
)

SKIP_DIRS = {
    os.path.join(ROOT, '.git'),
    os.path.join(ROOT, 'assets', 'vendor'),
    os.path.join(ROOT, 'venv'),
    os.path.join(ROOT, '.venv'),
}

def download(url, dest):
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(dest):
            return
        print(f"Downloading {url} to {dest}")
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def process_file(file_path):
    def local_for_url(url):
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path.lstrip('/')
        if parsed.query:
            path = f"{path}_{sanitize_query(parsed.query)}"
        local_path = os.path.join(OUT_DIR, host, path)
        return local_path

    def sanitize_query(query):
        if not query:
            return ''
        return re.sub(r'[^0-9A-Za-z._-]', '_', query)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def repl(match):
        prefix = match.group('prefix') or 'https:'
        host = match.group('host')
        path = match.group('path')
        url = prefix + '//' + host + path
        url = html.unescape(url)

        local_path = local_for_url(url)
        download(url, local_path)

        rel_path = os.path.relpath(local_path, os.path.dirname(file_path))
        return rel_path.replace('\\', '/')

    new_content = PATTERN.sub(repl, content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    # Example usage: process all html and js files in ROOT
    for root, dirs, files in os.walk(ROOT):
        if any(root.startswith(skip) for skip in SKIP_DIRS):
            continue
        for file in files:
            if file.endswith(('.html', '.js', '.css')):
                process_file(os.path.join(root, file))
