#!/usr/bin/env python3
"""Render the news-image-20261124 front page (1024x1024) in code.
All text comes from STORIES.md only. No AI image generation.
Copy is tightened to fit the page; every fact, number and source tag is kept.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14                      # outer margin
CW = W - 2 * M              # content width = 996
PAPER = (247, 242, 231)
INK = (22, 22, 22)
RED = (176, 30, 30)
GRAY = (96, 90, 78)
RULE = (70, 64, 50)
LIGHT = (235, 228, 212)
SEA = (214, 226, 232)
LAND = (216, 203, 168)
LAND_LINE = (150, 135, 105)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def hline(d, x0, x1, y, fill=RULE, w=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def section_head(d, y, text):
    d.text((M, y), text, font=font(FB, 12), fill=INK)
    y += 16
    hline(d, M, W - M, y, fill=RULE, w=1)
    return y + 4


# ---------------------------------------------------------------- icons
def icon_ship(d, x, y, w, h, ink=INK):
    d.polygon([(x + 4, y + h * 0.45), (x + w - 4, y + h * 0.45),
               (x + w - 12, y + h * 0.8), (x + 12, y + h * 0.8)], fill=ink)
    d.rectangle([x + w * 0.42, y + h * 0.18, x + w * 0.58, y + h * 0.45], fill=ink)
    d.line([(x + w * 0.5, y + 2), (x + w * 0.5, y + h * 0.18)], fill=ink, width=2)
    for yy in (h * 0.88, h * 0.97):
        d.arc([x, y + yy - 3, x + w, y + yy + 3], 0, 180, fill=(90, 110, 130), width=2)


def icon_tanker(d, x, y, w, h, ink=INK):
    d.rectangle([x + 3, y + h * 0.4, x + w - 3, y + h * 0.75], fill=ink)
    d.rectangle([x + w * 0.68, y + h * 0.15, x + w * 0.82, y + h * 0.4], fill=ink)
    d.line([(x + 2, y + h * 0.85), (x + w - 2, y + h * 0.85)], fill=RED, width=3)
    d.arc([x, y + h * 0.88 - 3, x + w, y + h * 0.88 + 3], 0, 180,
          fill=(90, 110, 130), width=2)


def icon_chip(d, x, y, w, h, ink=INK):
    s = min(w, h) * 0.62
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                outline=ink, width=3)
    d.rectangle([cx - s / 4, cy - s / 4, cx + s / 4, cy + s / 4], fill=RED)
    for i in range(3):
        off = -s / 4 + i * s / 4
        d.line([(cx + off, cy - s / 2 - 6), (cx + off, cy - s / 2)], fill=ink, width=2)
        d.line([(cx + off, cy + s / 2), (cx + off, cy + s / 2 + 6)], fill=ink, width=2)
        d.line([(cx - s / 2 - 6, cy + off), (cx - s / 2, cy + off)], fill=ink, width=2)
        d.line([(cx + s / 2, cy + off), (cx + s / 2 + 6, cy + off)], fill=ink, width=2)


def icon_badge(d, x, y, w, h, ink=INK):
    cx, cy = x + w / 2, y + h / 2
    r = min(w, h) * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=3)
    d.text((cx - 4, cy - 8), "*", font=font(FB, 16), fill=RED)


def icon_missile(d, x, y, w, h, ink=INK):
    d.polygon([(x + w * 0.5, y + 3), (x + w * 0.68, y + h * 0.45),
               (x + w * 0.6, y + h * 0.62), (x + w * 0.4, y + h * 0.62),
               (x + w * 0.32, y + h * 0.45)], fill=ink)
    d.polygon([(x + w * 0.5, y + h * 0.62), (x + w * 0.62, y + h * 0.85),
               (x + w * 0.38, y + h * 0.85)], fill=RED)


def icon_warn(d, x, y, w, h, ink=INK):
    cx = x + w / 2
    d.polygon([(cx, y + 3), (x + w - 3, y + h - 4), (x + 3, y + h - 4)],
              outline=ink, width=3)
    d.text((cx - 3, y + h * 0.42), "!", font=font(FB, 16), fill=RED)


def icon_ball(d, x, y, w, h, ink=INK, ball="foot"):
    cx, cy = x + w / 2, y + h / 2
    r = min(w, h) * 0.34
    if ball == "foot":
        d.ellipse([cx - r * 1.25, cy - r * 0.7, cx + r * 1.25, cy + r * 0.7],
                  outline=ink, width=3)
        d.line([(cx - r * 0.7, cy - r * 0.4), (cx + r * 0.7, cy + r * 0.4)],
               fill=ink, width=2)
        d.line([(cx - r * 0.7, cy + r * 0.4), (cx + r * 0.7, cy - r * 0.4)],
               fill=ink, width=2)
    else:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=3)
        d.arc([cx - r, cy - r * 0.4, cx + r, cy + r * 0.4], 200, 340,
              fill=ink, width=2)
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=ink, width=2)


def icon_capitol(d, x, y, w, h, ink=INK):
    cx = x + w / 2
    d.rectangle([x + 6, y + h * 0.62, x + w - 6, y + h * 0.7], fill=ink)
    d.arc([cx - 12, y + h * 0.2, cx + 12, y + h * 0.68], 180, 360,
          fill=ink, width=3)
    d.rectangle([x + 4, y + h * 0.72, x + w - 4, y + h * 0.82], fill=ink)
    for i in range(4):
        xx = x + 10 + i * (w - 20) / 3
        d.line([(xx, y + h * 0.72), (xx, y + h * 0.82)], fill=PAPER, width=2)


def icon_building(d, x, y, w, h, ink=INK):
    d.rectangle([x + w * 0.2, y + h * 0.15, x + w * 0.8, y + h * 0.85],
                outline=ink, width=3)
    d.line([(x + w * 0.5, y + h * 0.15), (x + w * 0.68, y + h * 0.5),
            (x + w * 0.55, y + h * 0.5), (x + w * 0.62, y + h * 0.85)],
           fill=RED, width=2)
    for r in range(2):
        for c in range(3):
            d.rectangle([x + w * (0.3 + c * 0.17), y + h * (0.3 + r * 0.22),
                         x + w * (0.3 + c * 0.17) + 4, y + h * (0.3 + r * 0.22) + 4],
                        fill=ink)


def icon_flags(d, x, y, w, h, ink=INK):
    for i, col in enumerate((RED, INK, (90, 110, 130))):
        fx = x + 6 + i * (w - 12) / 3
        d.line([(fx, y + 4), (fx, y + h - 4)], fill=ink, width=2)
        d.polygon([(fx, y + 4), (fx + (w - 12) / 3 - 2, y + 8),
                   (fx, y + 13)], fill=col)


def icon_satellite(d, x, y, w, h, ink=INK):
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - 7, cy - 5, cx + 7, cy + 5], outline=ink, width=2)
    d.polygon([(cx - 20, cy - 8), (cx - 8, cy - 4), (cx - 8, cy + 4),
               (cx - 20, cy + 8)], outline=ink, width=2)
    d.polygon([(cx + 8, cy - 4), (cx + 20, cy - 8), (cx + 20, cy + 8),
               (cx + 8, cy + 4)], outline=ink, width=2)
    for sx, sy in ((x + 4, y + 4), (x + w - 6, y + 6), (x + w - 10, y + h - 6)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=RED)


LEAD_ICONS = [icon_ship, icon_tanker, icon_chip]
CARD_ICONS = [icon_badge, icon_missile, icon_warn, icon_ball, icon_ball,
              icon_ball, icon_capitol, icon_building, icon_flags, icon_satellite]


# ---------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-75, 62), (-60, 55), (-55, 47), (-65, 45), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 22), (-97, 16),
     (-92, 15), (-86, 13), (-83, 9), (-79, 9), (-85, 11), (-90, 14),
     (-97, 16), (-105, 20), (-110, 23), (-114, 28), (-120, 34), (-125, 40),
     (-125, 49), (-130, 55), (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-20, 70), (-25, 76),
     (-40, 80), (-58, 76), (-60, 70)],
    [(-79, 9), (-72, 11), (-62, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-57, -35), (-62, -41),
     (-68, -50), (-70, -55), (-73, -50), (-73, -40), (-72, -30), (-70, -20),
     (-75, -15), (-80, -5), (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 68), (10, 64), (5, 60), (5, 58), (-2, 57), (-5, 50), (-8, 43)],
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (37, 22), (43, 12), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18),
     (32, -26), (28, -33), (20, -35), (15, -30), (12, -18), (12, -5),
     (9, 4), (0, 5), (-8, 5), (-15, 11)],
    [(30, 62), (35, 68), (45, 68), (60, 69), (75, 73), (90, 75), (110, 74),
     (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (160, 60),
     (158, 53), (150, 60), (142, 55), (140, 45), (135, 43), (130, 42),
     (127, 40), (122, 38), (120, 32), (115, 23), (108, 18), (105, 10),
     (100, 8), (98, 12), (95, 16), (90, 22), (85, 20), (80, 13), (77, 8),
     (73, 20), (70, 25), (66, 25), (62, 25), (57, 26), (52, 28), (50, 30),
     (48, 30), (44, 29), (40, 32), (36, 36), (33, 36), (30, 36), (27, 37),
     (23, 36), (26, 38), (28, 41), (30, 45), (30, 50), (30, 55)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (146, -39), (150, -37), (153, -32), (153, -27), (146, -19),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 41), (143, 42), (145, 44), (142, 45), (140, 42), (138, 38),
     (136, 36), (133, 35), (131, 33)],
]

PINS = [
    (1, 20, 32), (2, 56, 27), (3, -122, 37), (4, -107, 25), (5, 19, 52),
    (6, 25, 59), (7, -99, 19), (8, -74, 41), (9, -98, 29), (10, -118, 34),
    (11, 30, 51), (12, 114, 22), (13, 179, 78), (14, 30, 50), (15, -122, 44),
    (16, 31, 49), (17, 33, 48), (18, -77, 39), (19, 58, 28), (20, -77, 42),
    (21, -74, 40), (22, -84, 33), (23, -93, 42), (24, 34, 31), (25, 35, 32),
    (26, 4, 52), (27, 45, 40), (28, 10, 56), (29, 127, 37), (30, 124, 38),
    (31, 90, 24), (32, -116, 34), (33, 0, 51), (34, -105, 40),
    (35, 60, 29), (36, -6, 53),
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=RULE, width=1)
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360 * w
        d.line([(gx, y0), (gx, y0 + h)], fill=(200, 212, 220), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y0 + (85 - lat) / 145 * h
        d.line([(x0, gy), (x0 + w, gy)], fill=(200, 212, 220), width=1)

    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * w, y0 + (85 - lat) / 145 * h)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_LINE)

    placed = []
    fpin = font(FB, 8)
    # candidate label offsets (dx, dy) from the true position, tried in order:
    # spiral outwards so crowded clusters fan around the point instead of
    # marching off in one long horizontal chain.
    OFFSETS = [(0, 0), (14, 0), (-14, 0), (0, -14), (0, 14),
               (14, -14), (-14, -14), (14, 14), (-14, 14),
               (28, 0), (-28, 0), (0, -28), (0, 28),
               (28, -14), (-28, -14), (28, 14), (-28, 14),
               (14, -28), (-14, -28), (14, 28), (-14, 28),
               (28, -28), (-28, -28), (28, 28), (-28, 28),
               (42, 0), (-42, 0), (0, -42), (0, 42),
               (42, -14), (-42, -14), (42, 14), (-42, 14)]
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        if num == 13:
            lx, ly = x0 + w - 16, y0 + 10
        else:
            lx, ly = px, py
            for dx, dy in OFFSETS:
                cx, cy = px + dx, py + dy
                if not (x0 + 8 <= cx <= x0 + w - 8 and
                        y0 + 8 <= cy <= y0 + h - 8):
                    continue
                if all((cx - qx) ** 2 + (cy - qy) ** 2 >= 15 ** 2
                       for qx, qy in placed):
                    lx, ly = cx, cy
                    break
            else:
                lx, ly = px, py
        placed.append((lx, ly))
        if (lx, ly) != (px, py):
            d.line([(px, py), (lx, ly)], fill=INK, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        r = 7
        d.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(255, 255, 255),
                  outline=RED, width=1)
        t = str(num)
        tw = fpin.getlength(t)
        d.text((lx - tw / 2, ly - 5), t, font=fpin, fill=RED)


# ---------------------------------------------------------------- content
UTC_ITEMS = [
    ("01:20 UTC", "Kickoff 49ers–Vikings, Estadio Banorte, Mexico City (theScore)"),
    ("~06:00 UTC", "Ukraine air force: 134 of 153 Russian drones downed/jammed (08:00 Kyiv local)"),
    ("17:58 UTC", "Iran foreign minister vows to fight US blockade \u201cby all means\u201d (CBS, 12:58 ET)"),
    ("18:01 UTC", "Reuters: Zelensky confirms Ukraine sank the Merkury"),
    ("22:29 UTC", "NPR/AP: Rep. Jimmy Gomez announces resignation effective 1 Dec"),
    ("23:34 UTC", "NATO commits to stronger space defence (Russian nuclear satellite report)"),
    ("00:15 UTC", "Ukraine urges US on delayed Patriot deliveries"),
]

NUMBERS = [
    ("7", "Sea drones sank the corvette Merkury (Zelensky/AP)"),
    ("153", "Drones launched overnight; 134 downed (Ukraine Air Force)"),
    ("+33%", "Nvidia share jump; S&P 500 +4.82% (AP)"),
    ("$450M", "Skubal's Mets contract, richest pitcher deal ever (AP)"),
    ("35–10", "49ers over Vikings in Mexico City (AP)"),
    ("50", "Wembanyama points; Spurs 114–91 over Pelicans (AP)"),
]

LEADS = [
    ("1. UKRAINIAN SEA DRONES SINK RUSSIAN CORVETTE OFF LIBYA",
     "Seven Ukrainian sea drones sank the corvette Merkury (commissioned 2023) at the "
     "Benghazi naval base, Sunday 22 Nov; confirmed by Zelensky on Monday 23 Nov; a "
     "Ka-27 helicopter was also destroyed; cargo ship MV Angara was also hit; 10 people "
     "hurt (Libya + Russia).",
     "BENGHAZI, LIBYA", "CONFIRMED (AP / Reuters)"),
    ("2. IRAN VOWS \u201cALL MEANS\u201d AGAINST US BLOCKADE",
     "Iran's foreign minister: use all means against the US sea blockade; Trump (Fox "
     "News, Sunday): leans to resuming strikes after the New Year if there is no deal; "
     "CNN: attacks on shipping in Hormuz are the highest since the war began; Kpler: "
     "Iranian oil on the water fell to zero.",
     "TEHRAN / WASHINGTON", "CONFIRMED (CBS / Reuters / CNN)"),
    ("3. NVIDIA BRINGS BACK HUANG — AND WALL STREET ROARS",
     "Nvidia's board brought Jensen Huang back as president + CEO, 11 days after he "
     "stepped down amid an affair scandal with a woman suspected of being a Chinese "
     "spy; shares +~33%; S&P 500 +4.82%; the SEC is investigating Nvidia's accounting "
     "practices; Treasury Secretary Bessent wants answers on chip sales to China "
     "within ~10 days.",
     "SANTA CLARA, US", "CONFIRMED (AP / Reuters)"),
]

CARDS = [
    ("4. \u201cEL CHAPO ISIDRO\u201d CAPTURED IN SINALOA",
     "Mexican forces captured Fausto Isidro Meza Flores, a top-10 FBI fugitive; US "
     "drones assisted from over Mexico.",
     "CONFIRMED (AP)"),
    ("5. POLAND: THREE OBJECTS WERE RUSSIAN KH-101 MISSILES",
     "NATO's North Atlantic Council met in emergency session Mon 23 Nov; Rutte: "
     "NATO will defend every inch of Poland.",
     "CONFIRMED (Reuters / AP)"),
    ("6. MOSCOW: ESTONIA ON \u201cVERGE OF TRIGGERING OPEN WAR\u201d",
     "Moscow accuses Estonia of hostile actions.",
     "OFFICIAL (Reuters)"),
    ("7. 49ERS ROUT VIKINGS 35–10 IN MEXICO CITY",
     "Purdy 21/26, 255 yards, 3 TD; 49ers 9–1; first Sunday Night Football outside "
     "the US; 85,612 fans.",
     "CONFIRMED (AP / theScore)"),
    ("8. SKUBAL TO METS: $450M, RICHEST PITCHER DEAL EVER",
     "Two-time Cy Young winner, 9 years, pending physical; chose Mets over Blue "
     "Jays, Padres, Dodgers.",
     "CONFIRMED (AP)"),
    ("9. WEMBANYAMA'S 50-POINT NIGHT",
     "Spurs beat Pelicans 114–91; Wemby first since 1973–74 with 50 points, 15+ "
     "rebounds, 4 steals, 5 blocks.",
     "CONFIRMED (AP)"),
    ("10. REP. JIMMY GOMEZ TO RESIGN AFTER ETHICS REPORT",
     "House Ethics Committee found \u201csubstantial evidence\u201d of sexual "
     "misconduct; Gomez resigns 1 Dec, disputing it.",
     "CONFIRMED (AP / NPR)"),
    ("11. DYMER STRIKE DEATH TOLL RISES TO 11",
     "Russian drone strike partly destroyed an apartment block in Dymer, near Kyiv; "
     "14 had been reported missing.",
     "CONFIRMED (AP / Reuters)"),
    ("12. TRUMP CALLS PUTIN \u201cMY FRIEND\u201d AFTER SHENZHEN SUMMIT",
     "First Trump–Xi–Putin meeting in Shenzhen (~80 min, APEC sidelines); promises "
     "of nuclear-risk talks.",
     "REPORTED (Reuters / AP)"),
    ("13. NATO PLEDGES SPACE DEFENCE VS NUKE SATELLITE",
     "NATO intelligence: Russia plans to launch a nuclear-armed satellite this "
     "year; NATO to strengthen space defence.",
     "REPORTED (Reuters / Just Security)"),
]

BRIEFS_L = [
    ("14.", "Zelensky: intelligence shows Russia planning a new attack on Ukraine. REPORTED (Reuters)"),
    ("15.", "US to blacklist Megaspeed, a chip firm tied to the Nvidia scandal. REPORTED (Reuters)"),
    ("16.", "Russia launched 153 drones overnight into Monday; 134 downed/jammed (Ukraine AF). CONFIRMED (Reuters)"),
    ("17.", "Russian strike on Kryvyi Rih kills child + young woman; 25 apartment buildings damaged. CONFIRMED (AP)"),
    ("18.", "Ukraine urges US on delayed Patriot deliveries. OFFICIAL (24 Nov 00:15 UTC)"),
    ("19.", "Two tankers hit near Hormuz, Sat.; Iran blames sea mines; UKMTO reports damage. REPORTED (UKMTO)"),
    ("20.", "Democrats plan 12 debates for the 2028 presidential primary, the first in June. CONFIRMED (AP)"),
    ("21.", "FBI investigates the hack of the National Crime Information Center. REPORTED (23 Nov)"),
    ("22.", "Delta automation-system outage causes delays as Americans travel home for Thanksgiving. CONFIRMED (AP)"),
    ("23.", "Trump pauses a plan to detonate degraded explosives in Iowa (US Army). OFFICIAL (AFP)"),
    ("24.", "Israeli strikes in Gaza kill at least 3 people, including a UNRWA worker. CONFIRMED (Reuters)"),
    ("25.", "Israel PM-elect Eisenkot calls settler arson in West Bank \u201cJewish terrorism\u201d. OFFICIAL (Reuters)"),
]
BRIEFS_R = [
    ("26.", "14 countries \u201crecognise\u201d the ICJ ruling on the Rohingya genocide. CONFIRMED (Reuters)"),
    ("27.", "Armenia proposes a new constitution, a step toward peace with Azerbaijan. REPORTED (Reuters)"),
    ("28.", "Denmark to propose a phone ban in schools from 2027. OFFICIAL (Reuters)"),
    ("29.", "S. Korea's Lee Jae Myung reshuffles cabinet; Kang Kum-sil becomes first woman intelligence chief. OFFICIAL (23 Nov)"),
    ("30.", "S. Korea Education Minister Choi Kyo-jin resigns after anti-cheating AI rule for CSAT sparks protests. CONFIRMED (23 Nov)"),
    ("31.", "Bangladesh: will arrest and jail ex-PM Sheikh Hasina if she returns from India. OFFICIAL (Reuters)"),
    ("32.", "Miley Cyrus marries musician Maxx Morando, Saturday, in Palm Springs. REPORTED (23 Nov)"),
    ("33.", "Princess of Wales reflects on life after her 2024 cancer diagnosis in \u201cHeal\u201d. REPORTED (23 Nov)"),
    ("34.", "Tom Jackson, Broncos linebacker + ESPN analyst, dies at 75. CONFIRMED (23 Nov)"),
    ("35.", "British endurance athlete Lewis Pugh swims in the Strait of Hormuz. REPORTED (24 Nov)"),
    ("36.", "Gaza students to start university in Ireland after winning a visa dispute. REPORTED (24 Nov)"),
]

DATECHECK_L = ("Already in the 23 Nov edition: Iranian tanker convoy at Kharg (23 Nov "
               "headline); COP31 ending with no deal; Democrats winning 258 House seats; "
               "Trump Route launch; Tangerang factory fire, 3 dead 36 missing; Sparta II "
               "burning in the Baltic — heavily damaged, NOT sunk.")
DATECHECK_R = ("Too old for this edition (20–22 Nov): Peru M6.8 quake (Fri 20 Nov); boat "
               "capsized in Nigeria, 24 dead (Fri 20 Nov, reported 22 Nov); Basra power "
               "station fire, 4 dead 35 hurt (Sat 21 Nov); Spain extends bank tax (Sat "
               "21 Nov); UN talks on \u201ckiller robots\u201d (Sat 21 Nov); Phumzile "
               "Mlambo-Ngcuka dies aged 71 (Fri 20 Nov); student protests in Europe "
               "(Fri 20 Nov).")
DATECHECK_NOTYET = ("Not yet: US government funding vote (deadline 11 Dec) · Gomez formally "
                    "resigns (1 Dec) · Democrats take the House (3 Jan)")


# ---------------------------------------------------------------- render
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10

    # kicker + count + masthead
    f_kick = font(FB, 19)
    t = "ONE DAY OF WORLD NEWS, ONE PICTURE"
    d.text(((W - f_kick.getlength(t)) / 2, y), t, font=f_kick, fill=RED)
    y += 22
    f_cnt = font(FB, 11)
    t = "36 STORIES · 5 CONTINENTS + SPACE · 12 FIELDS · ALL FROM THIS TUESDAY"
    d.text(((W - f_cnt.getlength(t)) / 2, y), t, font=f_cnt, fill=INK)
    y += 14
    f_mast = font(SB, 48)
    t = "TUESDAY 24 NOVEMBER 2026"
    d.text(((W - f_mast.getlength(t)) / 2, y), t, font=f_mast, fill=INK)
    y += 54
    hline(d, M, W - M, y, fill=INK, w=3)
    y += 3
    hline(d, M, W - M, y, fill=INK, w=1)
    y += 7

    # ---- THE DAY IN UTC
    y = section_head(d, y, "THE DAY IN UTC")
    f_time = font(FB, 12)
    f_utc = font(FR, 11)
    for row in (UTC_ITEMS[:4], UTC_ITEMS[4:]):
        cw = CW // 4
        row_h = 0
        for i, (tm, txt) in enumerate(row):
            x = M + i * cw
            d.text((x, y), tm, font=f_time, fill=RED)
            lines = wrap(txt, f_utc, cw - 8)
            yy = y + 15
            for ln in lines[:2]:
                d.text((x, yy), ln, font=f_utc, fill=INK)
                yy += 13
            row_h = max(row_h, yy - y)
        y += row_h + 1
    # ---- THE DAY IN NUMBERS
    y = section_head(d, y, "THE DAY IN NUMBERS")
    f_num = font(SB, 24)
    f_nlab = font(FR, 9)
    cw = CW // 6
    top = y
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * cw
        nw = f_num.getlength(num)
        d.text((x + (cw - 10 - nw) / 2, y), num, font=f_num, fill=RED)
        lines = wrap(lab, f_nlab, cw - 10)
        yy = y + 29
        for ln in lines[:2]:
            d.text((x, yy), ln, font=f_nlab, fill=INK)
            yy += 10
        if i < 5:
            d.line([(x + cw - 4, y + 2), (x + cw - 4, yy - 2)], fill=RULE, width=1)
    y = top + 29 + 2 * 10 + 4

    # ---- 3 LEADS
    lw = (CW - 2 * 9) // 3
    lead_top = y
    for i, (head, body, loc, tag) in enumerate(LEADS):
        x = M + i * (lw + 9)
        d.rectangle([x, y, x + lw, y + 166], outline=RULE, width=1)
        d.rectangle([x + 1, y + 1, x + lw - 1, y + 46], fill=LIGHT)
        LEAD_ICONS[i](d, x + (lw - 110) / 2, y + 3, 110, 42)
        yy = y + 51
        f_h = font(FB, 12)
        for ln in wrap(head, f_h, lw - 12)[:2]:
            d.text((x + 6, yy), ln, font=f_h, fill=INK)
            yy += 14
        f_b = font(SR, 10)
        for ln in wrap(body, f_b, lw - 12)[:6]:
            d.text((x + 6, yy), ln, font=f_b, fill=INK)
            yy += 10
        f_t = font(FB, 9)
        d.text((x + 6, y + 166 - 20), loc, font=f_t, fill=GRAY)
        d.text((x + 6, y + 166 - 10), tag, font=f_t, fill=RED)
    y = lead_top + 166 + 5

    # ---- 10 CARDS (5 x 2), card height 88
    cw5 = (CW - 4 * 8) // 5
    card_h = 88
    for r in range(2):
        for c in range(5):
            i = r * 5 + c
            head, body, tag = CARDS[i]
            x = M + c * (cw5 + 8)
            yy = y + r * (card_h + 7)
            d.rectangle([x, yy, x + cw5, yy + card_h], outline=RULE, width=1)
            d.rectangle([x + 1, yy + 1, x + cw5 - 1, yy + 19], fill=LIGHT)
            if i in (3, 4, 5):
                CARD_ICONS[i](d, x + (cw5 - 34) / 2, yy + 1, 34, 18,
                              ball="foot" if i == 3 else "basket")
            else:
                CARD_ICONS[i](d, x + (cw5 - 34) / 2, yy + 1, 34, 18)
            ty = yy + 22
            f_h = font(FB, 9)
            for ln in wrap(head, f_h, cw5 - 10)[:2]:
                d.text((x + 5, ty), ln, font=f_h, fill=INK)
                ty += 11
            f_b = font(SR, 9)
            for ln in wrap(body, f_b, cw5 - 10)[:4]:
                d.text((x + 5, ty), ln, font=f_b, fill=INK)
                ty += 8
            d.text((x + 5, yy + card_h - 9), tag, font=font(FB, 8), fill=RED)
    y += 2 * card_h + 7 + 7

    # ---- MAP
    y = section_head(d, y, "WHERE IT HAPPENED")
    map_h = 88
    draw_map(d, M, y, CW, map_h)
    y += map_h + 4
    f_rc = font(FB, 11)
    t = "N. America 13  ·  Europe 11  ·  Middle East 5  ·  Asia 4  ·  Africa 1  ·  World + space 2"
    d.text(((W - f_rc.getlength(t)) / 2, y), t, font=f_rc, fill=INK)
    y += 13

    # ---- BRIEFS
    y = section_head(d, y, "ALSO ON TUESDAY")
    f_br = font(FR, 8)
    f_bn = font(FB, 8)
    col_w = (CW - 16) // 2
    by = y
    max_y = y
    for col, items in enumerate((BRIEFS_L, BRIEFS_R)):
        x = M + col * (col_w + 16)
        yy = by
        for num, txt in items:
            nw = f_bn.getlength(num + " ")
            d.text((x, yy), num, font=f_bn, fill=RED)
            ly = yy
            for ln in wrap(txt, f_br, col_w - nw):
                d.text((x + nw, ly), ln, font=f_br, fill=INK)
                ly += 10
            yy = ly
        max_y = max(max_y, yy)
    y = max_y + 1

    # ---- DATE CHECK
    y = section_head(d, y, "DATE CHECK — LEFT OUT ON PURPOSE")
    f_dc = font(FR, 9)
    col_w = (CW - 16) // 2
    ly = y
    for col, txt in enumerate((DATECHECK_L, DATECHECK_R)):
        x = M + col * (col_w + 16)
        yy = y
        for ln in wrap(txt, f_dc, col_w):
            d.text((x, yy), ln, font=f_dc, fill=GRAY)
            yy += 11
        ly = max(ly, yy)
    y = ly + 2
    d.text((M, y), DATECHECK_NOTYET, font=font(FB, 9), fill=INK)
    y += 10

    # ---- footer (one line)
    hline(d, M, W - M, y, fill=RULE, w=1)
    y += 5
    f_ft = font(FR, 9)
    d.text((M, y), "Sources: Reuters · AP · AFP · CBS · CNN · NPR · Ukraine Air Force · UKMTO — "
                   "CONFIRMED = wire-confirmed · OFFICIAL = on-the-record · REPORTED = single outlet",
           font=f_ft, fill=INK)
    y += 9

    print("final y =", y, "of", H)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
