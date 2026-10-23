"""Hammond wave 2b mocks + reference-vs-build QA (Brad 10-22 18:55 feedback + re-assessed dump items)."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/hats")
from teemock import place_print, sheet
from mock import front, sheet as hsheet
from PIL import Image, ImageDraw, ImageFont
HM = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm"
NAT, WHITE, BLACK, HEATHER, ORANGE = (236, 228, 210), (250, 250, 250), (28, 28, 30), (200, 200, 200), (226, 120, 54)
tees = [
    (f"{HM}/casa/casa_mark.png", NAT, 8.5, 2.5, "Casa de Fresa - FRONT: matchbook cover panel"),
    (f"{HM}/casa/casa_strawberries_green.png", NAT, 10.0, 3.0, "Casa de Fresa - BACK: inside cover (+ Five Efficiency Apartments)"),
    (f"{HM}/casaad/casa_ad_dixiehome.png", NAT, 10.0, 2.6, "Casa de Fresa - 'Your Dixie Home' listing ad"),
    (f"{HM}/galaxy/galaxy_pass_card.png", BLACK, 9.0, 2.6, "Galaxy Drive-In - courtesy pass (card), black tee"),
    (f"{HM}/galaxy/galaxy_pass_ink.png", NAT, 9.0, 2.6, "Galaxy Drive-In - courtesy pass, natural tee"),
    (f"{HM}/rushs2/rushs_ad_malts.png", NAT, 10.0, 2.6, "Rush's - 'Finest in Malts' ad"),
    (f"{HM}/cavetangi/cavetangi_napkin.png", WHITE, 8.5, 2.3, "Cave Tangi Restaurants - napkin, white tee"),
    (f"{HM}/fiesta/fiesta_club_logo.png", ORANGE, 10.0, 2.8, "Fiesta Club - logotype, orange tee"),
]
sheet([place_print(p, g, print_w_in=w, W=720, top_in=t, label=l) for p, g, w, t, l in tees], cols=4).save(f"{HM}/mocks_wave2b_tees.jpg", quality=86)
STONE = (196, 182, 150)
hsheet([front(f"{HM}/casa/hat_casadefresa_red.png", STONE, "Casa de Fresa - red (#CC3333) on stone (counters restored)"),
        front(f"{HM}/casa/hat_casadefresa_white.png", (176, 40, 52), "Casa de Fresa - white on red")], 2, f"{HM}/mocks_wave2b_hats.jpg")
a = Image.open(f"{HM}/casa/sock_casadefresa_front.png"); b = Image.open(f"{HM}/casa/sock_casadefresa_back.png")
S = Image.new("RGB", (a.width * 2 + 80, a.height + 120), (255, 255, 255)); S.paste(a, (0, 120)); S.paste(b, (a.width + 80, 120))
d = ImageDraw.Draw(S); f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
d.text((10, 20), "FRONT", fill=(60, 60, 60), font=f); d.text((a.width + 90, 20), "BACK", fill=(60, 60, 60), font=f)
S.thumbnail((900, 1900)); S.save(f"{HM}/mocks_wave2b_socks.jpg", quality=88)
def board(pairs, out, title):
    H = 560; ims = []
    for ref, build, lab in pairs:
        r = Image.open(ref).convert("RGB"); r.thumbnail((760, H))
        bi = Image.open(build).convert("RGBA"); bg = Image.new("RGB", bi.size, (236, 228, 210)); bg.paste(bi, (0, 0), bi); bg.thumbnail((760, H))
        ims.append((r, bg, lab))
    W = max(r.width + b.width for r, b, _ in ims) + 60
    S = Image.new("RGB", (W, sum(max(r.height, b.height) + 60 for r, b, _ in ims) + 60), (255, 255, 255)); d = ImageDraw.Draw(S)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    d.text((20, 15), title, fill=(0, 0, 0), font=f); y = 50
    for r, b, lab in ims:
        d.text((20, y), "reference  |  build:  " + lab, fill=(90, 90, 90), font=f); y += 28
        S.paste(r, (20, y)); S.paste(b, (40 + r.width, y)); y += max(r.height, b.height) + 32
    S.save(out, quality=88)
board([(f"{HM}/casaad/c7169.png", f"{HM}/casaad/casa_ad_dixiehome.png", "Casa listing ad (headline traced, small copy re-set, photo re-screened, names line off)"),
       (f"{HM}/galaxy/g7188.png", f"{HM}/galaxy/galaxy_pass_card.png", "Galaxy pass (all lines traced, phone off)"),
       (f"{HM}/rushs2/ad7180.png", f"{HM}/rushs2/rushs_ad_malts.png", "Rush's malts ad (type traced, photo re-screened)")],
      f"{HM}/qa_wave2b_ads.jpg", "Hammond wave 2b - reference vs build (1/2)")
board([(f"{HM}/cavetangi/ct7198.png", f"{HM}/cavetangi/cavetangi_napkin.png", "Cave Tangi napkin (traced; wing closed along the mug edge, I rebuilt, phones off)"),
       (f"{HM}/fiesta/ref_logo.png", f"{HM}/fiesta/fiesta_club_logo.png", "Fiesta Club logotype (traced; mascot + phone off)")],
      f"{HM}/qa_wave2b_other.jpg", "Hammond wave 2b - reference vs build (2/2)")
print("ok")
