#!/usr/bin/env python3
"""S9 part A sweep for SFV wave 2 masters (sfv/wave2), at the true print width recorded in each .prov.json
(the width the master is placed at in Printful, L40). Usage: python3 toolkit/sweep_sfv_w2.py [OUTDIR]"""
import glob, json, os, subprocess, sys
D = os.path.join(os.path.dirname(__file__), '..', 'sfv', 'wave2')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, 'qa')
rows, bad = [], 0
for png in sorted(glob.glob(os.path.join(D, 'sfv_*.png'))):
    prov = json.load(open(png[:-4] + '.prov.json'))
    w = prov['print_width_in']
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'art_qa.py'), png, '--width-in', str(w), '--out', OUT],
                       capture_output=True, text=True)
    q = json.load(open(os.path.join(OUT, os.path.basename(png)[:-4] + '_qa.json')))
    ok = r.returncode == 0
    bad += not ok
    rows.append((os.path.basename(png), w, prov.get('ink'), q['verdict'], q['fails'], q['warns'], q['exemptions'], q['typeset'], q['redrawn']))
    print(f"{'PASS' if ok else 'FAIL'}  {os.path.basename(png):34s} {w:6.2f} in  ink {prov.get('ink')}  fails {q['fails']} warns {q['warns']} exempt {q['exemptions']} typeset {q['typeset']} redrawn {q['redrawn']}")
json.dump(rows, open(os.path.join(OUT, 'sweep_sfv_w2.json'), 'w'), indent=1)
print(f"{len(rows)} masters, {bad} failing")
sys.exit(1 if bad else 0)
