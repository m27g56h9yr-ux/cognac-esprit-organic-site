#!/usr/bin/env python3
"""Private read-back/export; token stays in the local key file, never in URL/history."""
import argparse
import json
import os
from pathlib import Path
import sys
import urllib.request
import urllib.parse

parser = argparse.ArgumentParser(description='Contacts consentis Cognac Esprit Organic')
parser.add_argument('--export', type=Path, help='CSV destination outside the repository (created with mode 0600)')
parser.add_argument('--proofs', action='store_true', help='Export encrypted-store consent evidence instead of the common address book (requires --export)')
parser.add_argument('--cards', action='store_true', help='Card counters as JSON or CSV with --export')
parser.add_argument('--from-date', help='First UTC day, YYYY-MM-DD (requires --cards)')
parser.add_argument('--to-date', help='Last UTC day, YYYY-MM-DD (requires --cards)')
parser.add_argument('--token-file', type=Path, default=Path.home()/'.config/cognac-esprit-organic/salon-admin.token')
args = parser.parse_args()
if args.proofs and not args.export:
    parser.error('--proofs requires --export')
if args.cards and args.proofs:
    parser.error('--cards and --proofs are mutually exclusive')
if (args.from_date or args.to_date) and not args.cards:
    parser.error('Date filters require --cards')
repo = Path(__file__).resolve().parents[1]
if args.export:
    target = args.export.expanduser().resolve()
    if target == repo or repo in target.parents:
        parser.error('Choose an export location outside the Git repository.')
    if target.exists(): parser.error('The export destination already exists; choose a new filename.')
try:
    token = args.token_file.read_text().strip()
    query = {}
    if args.export: query['format'] = 'proofs' if args.proofs else 'csv'
    if args.cards: query['report'] = 'cards'
    if args.from_date: query['from'] = args.from_date
    if args.to_date: query['to'] = args.to_date
    url = 'https://cognac-esprit-organic.com/api/salon-admin.php' + ('?' + urllib.parse.urlencode(query) if query else '')
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer '+token, 'Accept':'text/csv' if args.export else 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read()
    if args.export:
        fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'wb') as f: f.write(data)
        print('Private export saved:', target)
    else:
        result = json.loads(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as error:
    print('Private salon access failed ('+type(error).__name__+'). No token was displayed.', file=sys.stderr)
    sys.exit(1)
