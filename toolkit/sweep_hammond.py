#!/usr/bin/env python3
"""Run the S9 art gate over every Hammond master in production. Usage: sweep_hammond.py OUTDIR [ARTDIR_OVERRIDES...]"""
import sys, os, json
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
import art_qa
W = os.path.join(os.path.dirname(__file__), '..', 'hammond', 'wave2')
# (product, master, print width in, exemptions, previous master for the SURVIVAL/TYPESET compare - required for every changed master)
PROD = [   # production masters after the 10-25 S9 pass (v1 kept beside each until Brad approves)
    ('casa F/B tee - front', 'casa_mark_v2.png', 8.5, [], 'casa_mark.png'),
    ('casa F/B tee - back', 'casa_strawberries_v2_green.png', 10, [], 'casa_strawberries_green.png'),
    ('casa Dixie Home ad tee', 'casa_ad_dixiehome_v2.png', 9.5, [], 'casa_ad_dixiehome.png'),
    ('toggery merged tee - front (left chest)', 'toggery_logo_leftchest_wine_v2.png', 3.5, [], 'toggery_logo_leftchest_wine.png'),
    ('toggery merged tee - back (blade sign)', 'toggery_sign_1color_wine_v2.png', 5.0, [], 'toggery_sign_1color_wine.png'),
    ('joy courtesy pass tee', 'joy_pass_ink_v3.png', 9, [], 'joy_pass_ink.png'),
    ('galaxy courtesy pass card tee', 'galaxy_pass_card_v2.png', 9, [], 'galaxy_pass_card.png'),
    ('galaxy courtesy pass tee - natural', 'galaxy_pass_ink_v2.png', 9, [], 'galaxy_pass_ink.png'),
    ("rush's drive-in tee", 'rushs_ad_v2.png', 10, [], 'rushs_ad.png'),
    ('didi-wa sign tee', 'didiwa_sign_charcoal_v2.png', 9.5, [], 'didiwa_sign_charcoal.png'),
    ('fiesta club tee', 'fiesta_club_logo_v3.png', 10, [], 'fiesta_club_logo.png'),
    ('magnolia inn sign tee', 'magnolia_sign_hammond_v5.png', 8.8, [], 'magnolia_sign_hammond.png'),
    ('casa hat (embroidery) - v1 kept', 'hats/hat_casadefresa_hammond_red.png', 4.74, [], None),
    ('toggery hat (embroidery)', 'hats/hat_toggery_maroon_v2.png', 3.67, [], 'hats/hat_toggery_maroon.png'),
    ('casa socks - front (v1 kept)', 'socks/sock_casadefresa_front.png', 1347 / 300, [], None),
    ('casa socks - back (v1 kept)', 'socks/sock_casadefresa_back.png', 1347 / 300, [], None),
]
def one(args):
    name, f, w, ex, prev, out, override = args
    path = override.get(f, os.path.join(W, f))
    r = art_qa.run(path, w, out, os.path.splitext(os.path.basename(f))[0], ex,
                   compare=os.path.join(W, prev) if prev else None)
    return name, f, r
if __name__ == '__main__':
    out = sys.argv[1]
    override = dict(a.split('=', 1) for a in sys.argv[2:])
    with ProcessPoolExecutor(6) as ex:
        res = list(ex.map(one, [(n, f, w, e, p, out, override) for n, f, w, e, p in PROD]))
    summary = []
    for name, f, r in res:
        summary.append(dict(product=name, master=f, verdict=r['verdict'], fails=r['fails'], warns=r['warns']))
        print(f"{r['verdict']:4s}  {name:42s} {f}")
        for x in r['fails']: print('        FAIL', x)
        for x in r['warns']: print('        warn', x)
    json.dump(summary, open(os.path.join(out, 'SWEEP.json'), 'w'), indent=1)
