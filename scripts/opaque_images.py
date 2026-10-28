#!/usr/bin/env python3
"""List a town's Shopify product images that are opaque photos (the catalog's OPAQUE_IMAGES).

Printful publishes most views as transparent PNG cut-outs (flat front, on-model, close-up, folded) and the
storefront gives those a soft drop-shadow (.hb-cut). The lifestyle view is an opaque photo with a studio
background, and a shadow around a rectangle looks wrong, so the catalog marks images listed here cut:false.

An image is opaque when its four corner pixels are fully opaque (alpha 255), or when it has no alpha channel
at all (JPG, RGB PNG). Each image is fetched from the Shopify CDN at width=64, so a run is quick.
A local knock-out (src/v2/product-images.json) still wins over this list in the catalog.

Usage (from the repo root; re-run after new mockups are published to Shopify):
  python3 scripts/opaque_images.py                  # Hattiesburg: writes src/v2/opaque-images.json
  python3 scripts/opaque_images.py --town hammond   # Hammond: writes src/v2/towns/hammond-opaque-images.json
  python3 scripts/opaque_images.py --town sfv       # San Fernando Valley: writes src/v2/towns/sfv-opaque-images.json
  python3 scripts/opaque_images.py --dry-run        # prints the list only
"""
import argparse
import io
import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

DOMAIN = 'nostalgic-towns.myshopify.com'
# Public Storefront token (the same one src/config/site.config.ts ships to browsers). The env var wins.
TOKEN = os.environ.get('SHOPIFY_STOREFRONT_TOKEN') or '26b7dcdc20879364ff735fbc45846857'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOWNS = {
    'hattiesburg': {
        'query': "tag:'town:hattiesburg'",
        'include': lambda tags: True,
        'out': 'src/v2/opaque-images.json',
    },
    # Same selection as src/v2/towns/hammond.ts: the pilot's untagged products, plus town:hammond and town:hammond-next.
    'hammond': {
        'query': None,
        'include': lambda tags: (lambda t: not t or 'town:hammond' in t or 'town:hammond-next' in t)(
            [x.strip().lower() for x in tags if x.strip().lower().startswith('town:')]),
        'out': 'src/v2/towns/hammond-opaque-images.json',
    },
    'sfv': {
        'query': "tag:'town:sfv'",
        'include': lambda tags: True,
        'out': 'src/v2/towns/sfv-opaque-images.json',
    },
}


def gql(query):
    req = urllib.request.Request(
        f'https://{DOMAIN}/api/2025-01/graphql.json', data=json.dumps({'query': query}).encode(),
        headers={'Content-Type': 'application/json', 'X-Shopify-Storefront-Access-Token': TOKEN})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    if not d.get('data'):
        sys.exit('Storefront API error: ' + json.dumps(d.get('errors') or d)[:400])
    return d['data']


def products(town):
    out, after = [], None
    while True:
        args = 'first: 250' + (f', after: {json.dumps(after)}' if after else '') + (f", query: {json.dumps(town['query'])}" if town['query'] else '')
        d = gql(f'{{ products({args}) {{ pageInfo {{ hasNextPage endCursor }} nodes {{ handle tags images(first: 50) {{ nodes {{ url }} }} }} }} }}')['products']
        out += [n for n in d['nodes'] if town['include'](n['tags'] or [])]
        if not d['pageInfo']['hasNextPage']:
            return out
        after = d['pageInfo']['endCursor']


def basename(url):
    # Same key as localFor() in src/v2/catalog.ts: file name without query string or extension.
    return re.sub(r'\.[a-z]+$', '', url.split('?')[0].split('/')[-1], flags=re.I)


def is_opaque(url):
    # Ask for PNG/JPEG (the CDN would otherwise negotiate WebP/AVIF from the Accept header).
    req = urllib.request.Request(url + ('&' if '?' in url else '?') + 'width=64', headers={'Accept': 'image/png,image/jpeg;q=0.9'})
    with urllib.request.urlopen(req, timeout=60) as r:
        im = Image.open(io.BytesIO(r.read()))
        im.load()
    if im.format != 'PNG' or not (im.mode in ('RGBA', 'LA', 'PA') or 'transparency' in im.info):
        return True
    a = im.convert('RGBA').getchannel('A')
    w, h = a.size
    return all(a.getpixel(xy) == 255 for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--town', default='hattiesburg', choices=sorted(TOWNS))
    ap.add_argument('--dry-run', action='store_true', help='print the list, write nothing')
    args = ap.parse_args()
    town = TOWNS[args.town]

    urls = {}
    for p in products(town):
        for im in p['images']['nodes']:
            urls.setdefault(basename(im['url']), im['url'])
    with ThreadPoolExecutor(8) as ex:
        flags = dict(zip(urls, ex.map(is_opaque, urls.values())))
    opaque = sorted(b for b, o in flags.items() if o)

    print(f'{args.town}: {len(urls)} images, {len(opaque)} opaque', file=sys.stderr)
    for b in opaque:
        print('  ' + b, file=sys.stderr)
    if args.dry_run:
        return
    path = os.path.join(ROOT, town['out'])
    with open(path, 'w') as f:
        f.write(json.dumps(opaque, indent=0) + '\n')
    print(f'wrote {os.path.relpath(path, ROOT)}', file=sys.stderr)


if __name__ == '__main__':
    main()
