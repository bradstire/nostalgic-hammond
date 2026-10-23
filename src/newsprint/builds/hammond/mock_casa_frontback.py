"""Casa de Fresa front/back tee: front = the matchbook's outside cover panel, back = its inside cover type."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from teemock import place_print, sheet, chest
HM = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm"
NAT = (236, 228, 210)
f = place_print(f"{HM}/casa/casa_mark.png", NAT, print_w_in=8.5, W=760, top_in=2.5, label="FRONT - matchbook cover panel, 8.5 in")
b = place_print(f"{HM}/casa/casa_strawberries_green.png", NAT, print_w_in=10.0, W=760, top_in=3.0, label="BACK - inside cover, 10 in")
sheet([f, b], cols=2).save(f"{HM}/mock_casa_frontback.jpg", quality=88)
print("ok")
