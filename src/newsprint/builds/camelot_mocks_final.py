"""Camelot final set (Brad 10-22 13:34): outline kept on the 1970s bag arch only; 1974 sign + tri-stripe solid."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from teemock import place_print, sheet
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/camelot"
NAT, WHITE, BLACK, GREY = (236, 228, 210), (250, 250, 250), (28, 28, 30), (200, 200, 200)
combos = [("camelot_v3_bag1974", NAT, 9.5, "Natural tee / 1970s bag arch (outlined - the one outlined design)"),
          ("camelot_v3_bag1974", WHITE, 9.5, "White tee / 1970s bag arch (outlined)"),
          ("camelot_v3_sign_red_blue", WHITE, 10.0, "White tee / 1974 sign line, solid red + blue locator"),
          ("camelot_v3_sign_red_white", BLACK, 10.0, "Black tee / 1974 sign line, solid red + white locator"),
          ("camelot_v3_tristripe", WHITE, 10.0, "White tee / tri-stripe, solid"),
          ("camelot_v3_tristripe", GREY, 10.0, "Heather grey / tri-stripe, solid")]
sheet([place_print(f"{D}/{f}.png", g, print_w_in=w, W=720, top_in=2.5, label=l) for f, g, w, l in combos], cols=3).save(f"{D}/camelot_v3_mocks.jpg", quality=88)
print("ok")
