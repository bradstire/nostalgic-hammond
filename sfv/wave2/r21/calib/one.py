import sys, json
sys.path.insert(0, '/home/claude/sfv2/calib')
from edge_metrics import region
f, box = sys.argv[1], [int(v) for v in sys.argv[2].split(',')]
m = region(f, box)
print(json.dumps(m))
