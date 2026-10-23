"""Hammond wave 2 mockups + reference-vs-build QA boards."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/hats")
from teemock import place_print, sheet
from mock import front, sheet as hsheet
from PIL import Image, ImageDraw, ImageFont
HM = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm"
NAT, WHITE, BLACK, CREAM, HEATHER, MAROON = (236, 228, 210), (250, 250, 250), (28, 28, 30), (240, 232, 214), (200, 200, 200), (104, 30, 40)
tees = [
    (f"{HM}/casa/casa_matchbook_cover_natural.png", NAT, 8.5, 2.5, "Casa de Fresa - matchbook cover, natural tee"),
    (f"{HM}/casa/casa_mark.png", WHITE, 9.0, 2.5, "Casa de Fresa - panel + ribbon, white tee"),
    (f"{HM}/casa/casa_strawberries_green.png", NAT, 10.0, 2.5, "Casa de Fresa - 'Land of Strawberries', natural"),
    (f"{HM}/toggery/toggery_sign.png", NAT, 5.0, 2.2, "Toggery Shop - neon blade sign, natural"),
    (f"{HM}/toggery/toggery_logo_address_wine.png", NAT, 9.0, 2.5, "Toggery Shop - ad logotype + address"),
    (f"{HM}/joy/joy_pass_card.png", BLACK, 9.0, 2.5, "Joy Drive-In - courtesy pass (card), black tee"),
    (f"{HM}/joy/joy_pass_ink.png", NAT, 9.0, 2.5, "Joy Drive-In - courtesy pass, natural tee"),
    (f"{HM}/didiwa/didiwa_sign_charcoal.png", NAT, 9.5, 2.5, "Didi-Wa Restaurant - sign, natural tee"),
    (f"{HM}/magnolia/magnolia_sign.png", WHITE, 8.0, 2.2, "Magnolia Inn - roadside sign, white tee"),
    (f"{HM}/rushs/rushs_ad.png", NAT, 10.0, 2.3, "Rush's - 'Louisiana's Finest Drive In' ad"),
    (f"{HM}/casa/casa_mark_leftchest.png", HEATHER, 3.5, 2.6, "Casa de Fresa - left chest, heather"),
    (f"{HM}/toggery/toggery_logo_leftchest_wine.png", CREAM, 3.5, 2.6, "Toggery Shop - left chest, cream"),
]
sheet([place_print(p, g, print_w_in=w, W=720, top_in=t, label=l) for p, g, w, t, l in tees], cols=4).save(f"{HM}/mocks_tees.jpg", quality=86)
STONE, KHAKI, CRANBERRY, WHITEH = (196, 182, 150), (186, 168, 128), (122, 32, 48), (244, 242, 236)
hsheet([front(f"{HM}/casa/hat_casadefresa_red.png", STONE, "Casa de Fresa - red (#CC3333) on stone"),
        front(f"{HM}/casa/hat_casadefresa_white.png", (176, 40, 52), "Casa de Fresa - white on red"),
        front(f"{HM}/toggery/hat_toggery_maroon.png", STONE, "Toggery Shop - maroon (#660000) on stone"),
        front(f"{HM}/toggery/hat_toggery_white.png", CRANBERRY, "Toggery Shop - white on cranberry")], 2, f"{HM}/mocks_hats.jpg")
a = Image.open(f"{HM}/casa/sock_casadefresa_front.png"); b = Image.open(f"{HM}/casa/sock_casadefresa_back.png")
S = Image.new("RGB", (a.width * 2 + 80, a.height + 120), (255, 255, 255)); S.paste(a, (0, 120)); S.paste(b, (a.width + 80, 120))
d = ImageDraw.Draw(S); f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
d.text((10, 20), "FRONT", fill=(60, 60, 60), font=f); d.text((a.width + 90, 20), "BACK", fill=(60, 60, 60), font=f)
S.thumbnail((900, 1900)); S.save(f"{HM}/mocks_socks.jpg", quality=88)

# reference vs build boards
def board(pairs, out, title):
    H = 520; ims = []
    for ref, build, lab in pairs:
        r = Image.open(ref).convert("RGB"); r.thumbnail((700, H))
        bi = Image.open(build).convert("RGBA"); bg = Image.new("RGB", bi.size, (236, 228, 210)); bg.paste(bi, (0, 0), bi); bg.thumbnail((700, H))
        ims.append((r, bg, lab))
    W = max(r.width + b.width for r, b, _ in ims) + 60
    S = Image.new("RGB", (W, sum(max(r.height, b.height) + 60 for r, b, _ in ims) + 60), (255, 255, 255)); d = ImageDraw.Draw(S)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    d.text((20, 15), title, fill=(0, 0, 0), font=f); y = 50
    for r, b, lab in ims:
        d.text((20, y), "reference  |  build:  " + lab, fill=(90, 90, 90), font=f); y += 28
        S.paste(r, (20, y)); S.paste(b, (40 + r.width, y)); y += max(r.height, b.height) + 32
    S.save(out, quality=88)
board([(f"{HM}/casa/matchbook_front_crop.png", f"{HM}/casa/casa_matchbook_cover_natural.png", "matchbook cover"),
       (f"{HM}/casa/matchbook_inside_crop.png", f"{HM}/casa/casa_strawberries_green.png", "inside cover type")],
      f"{HM}/qa_casa.jpg", "Casa de Fresa Hotel - reference vs build")
board([(f"{HM}/toggery/sign_crop.png", f"{HM}/toggery/toggery_sign.png", "blade sign (redrawn flat)"),
       (f"{HM}/toggery/ad_logo_crop.png", f"{HM}/toggery/toggery_logo_address_wine.png", "ad logotype (traced)")],
      f"{HM}/qa_toggery.jpg", "Toggery Shop - reference vs build")
board([(f"{HM}/joy/joy_pass_crop.png", f"{HM}/joy/joy_pass_card.png", "courtesy pass (no phone, no signature)"),
       (f"{HM}/didiwa/sign_crop.png", f"{HM}/didiwa/didiwa_sign_charcoal.png", "Didi-Wa sign (rectified, letters traced)"),
       (f"{HM}/magnolia/sign_crop.png", f"{HM}/magnolia/magnolia_sign.png", "Magnolia Inn sign (rectified, letters traced, emblem redrawn)"),
       (f"{HM}/rushs/ad_crop.png", f"{HM}/rushs/rushs_ad.png", "Rush's ad (re-typeset, photo re-screened)")],
      f"{HM}/qa_others.jpg", "Joy Drive-In / Didi-Wa / Magnolia Inn / Rush's - reference vs build")
print("ok")
