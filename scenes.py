"""All scenes of 'SAP Agents, part 2'. Each builder returns draw(frame, t)."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from chrome import *


# ---------------------------------------------------------------- split panel (banner + about) ----
@lru_cache(None)
def split_bg(split=1180):
    img = Image.new("RGB", (W, H), WHITE)
    col = Image.new("RGB", (1, H))
    for y in range(H): col.putpixel((0, y), mix(AZURE, VIOLET, y / H))
    img.paste(col.resize((W - split, H)), (split, 0))
    ov = SS(W - split, H, k=1)
    for y in range(30, H, 30):
        for x in range(20, W - split, 30): ov.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 255, 255, 34))
    ov.ellipse((360, -260, 1100, 480), outline=(255, 255, 255, 60), width=3); ov.ellipse((-200, 640, 520, 1360), fill=(255, 255, 255, 18))
    o = ov.done(); img.paste(o, (split, 0), o)
    s = SS(W, 12, k=1); s.rect((0, 0, split, 8), fill=ACC); o = s.done(); img.paste(o, (0, H - 8), o)
    return img


def big_chip(text, size, fill, fg):
    w = int(tw(text, size, True)) + int(size * 0.55); h = int(size * 1.42)
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((30, 42, 30 + w, 42 + h), int(size * .28), fill=(20, 30, 90, 80)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    s = SS(w + 60, h + 60); s.rr((30, 30, 30 + w, 30 + h), int(size * .28), fill=fill); s.text((30 + w / 2, 30 + h / 2 + size * .04), text, size, fg, bold=True, anchor="mm")
    im.alpha_composite(s.done()); return im, w


def build_banner(T, st, sents):
    bg = split_bg()
    kb = SS(1040, 40); kb.text((2, 4), "INDEPENDENT DEMO  ·  SAP BTP TRIAL  ·  PART 2", 24, ACC, bold=True, spacing=3); kicker = L(kb.done(), 120, 110)
    size = 150
    while True:
        a_im, sw = big_chip("SAP", size, AZURE, WHITE); b_im, aw = big_chip("Agents", size, ACC, WHITE)
        if sw + 36 + aw <= 1000: break
        size -= 6
    chip_sap = L(a_im, 120 - 30, 170 - 30); chip_ag = L(b_im, 120 + sw + 36 - 30, 170 - 30)
    line2 = text_layer(122, 430, "that say so when systems disagree.", 60, INK, bold=True)
    sub = text_layer(124, 520, ["An independent ledger, a BTP destination and a chained", "audit trail, built live on SAP BTP."], 32, MUTE)
    chips = []; cx = 122
    for txt, fg, bgc, ol in (("Independent ledger", (0, 110, 118), PALEACC, ACC), ("BTP destination", AZURE, PALE, AZURE), ("Chained audit trail", INDIGO, (234, 232, 250), VIOLET)):
        c = chip(cx, 650, txt, 25, fg=fg, bg=bgc, outline=ol); chips.append(c); cx += c.w + 10

    def tile(y, head, val, sub_, col):
        c = card(1260, y, 580, 190, r=20); s = SS(580, 190)
        s.text((34, 24), head, 24, MUTE, bold=True); s.text((34, 62), val, 92, col, bold=True); s.text((250, 100), sub_, 24, TEXT)
        c.im.alpha_composite(s.done(), (26, 26)); return c
    t1 = tile(210, "STOCK SERVICE  ·  SAP HANA", "8.8", "material 42 available", INK)
    t2 = tile(450, "INDEPENDENT LEDGER", "9.1", "same material, other system", INK)
    mm = chip(1260, 690, "MISMATCH  flagged, not hidden", 30, fg=WHITE, bg=RED, padx=26, pady=12)

    def draw(f, t):
        f.paste(bg, (0, 0)); appear(f, kicker, t, 0.15)
        pop(f, chip_sap, t, 0.4, 0.55); pop(f, chip_ag, t, 0.8, 0.55)
        if t > 1.4:
            p = ease_out(prog(t, 1.4, 0.6)); x0 = 120 + sw + 36 + 8; ImageDraw.Draw(f).rounded_rectangle((x0, 398, x0 + max(6, int((aw - 16) * p)), 408), 5, fill=VIOLET)
        appear(f, line2, t, 1.3); appear(f, sub, t, 1.9)
        for i, c in enumerate(chips): appear(f, c, t, 2.5 + i * 0.3)
        t0 = st[1] if len(st) > 1 else 3.0
        appear(f, t1, t, t0 + 0.2, 0.5); appear(f, t2, t, t0 + 1.0, 0.5); pop(f, mm, t, t0 + 2.0, 0.5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- recap: the standard Joule build ----
def build_recap(T, st, sents):
    base = shell("Recap"); tl = title("Where this started: the standard Joule Studio build", "Following SAP's learning journey, step by step")
    dv, _, _ = shot_card("joule_dest_var", 1100, 212, 340)
    sk, _, _ = shot_card("joule_skill", 1500, 212, 340)
    l1 = chip(1100, 212 + dv.h - 30, "1  Destination variable", 22, fg=AZURE, bg=PALE, outline=AZURE)
    l2 = chip(1500, 212 + sk.h - 30, "2  One skill per operation", 22, fg=AZURE, bg=PALE, outline=AZURE)
    tools, _, _ = shot_card("joule_tools", CX0, 212, 880)
    l3 = chip(CX0, 212 + tools.h - 20, "3  Five tools attached to one agent", 22, fg=AZURE, bg=PALE, outline=AZURE)
    ans, sc, org = shot_card("joule_answer", 1100, 560, 740)
    wrong = chip(1116, 830, "The model did the arithmetic", 21, fg=RED, bg=PALERED, outline=RED)
    moved = card(CX0, 760, 880, 120, r=16, accent=ACC); s = SS(880, 120)
    s.text((30, 26), "Video 1: the arithmetic moved into a governed SAP service", 25, INK, bold=True)
    s.text((30, 66), "Verdict computed in code  ·  every call written to an audit trail on SAP HANA", 21, MUTE); moved.im.alpha_composite(s.done(), (26, 26))

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        appear(f, dv, t, st[1] + 0.1, 0.5); appear(f, l1, t, st[1] + 0.4)
        appear(f, sk, t, st[1] + 1.6, 0.5); appear(f, l2, t, st[1] + 1.9)
        appear(f, tools, t, st[1] + 3.1, 0.6); appear(f, l3, t, st[1] + 3.5)
        appear(f, ans, t, st[2] + 0.1, 0.6); appear(f, wrong, t, st[2] + 4.2)
        callout(f, t, st[2] + 1.6, (568, 96, 772, 182), sc, org, col=GREEN, num=None)
        callout(f, t, st[2] + 3.6, (572, 394, 1126, 426), sc, org, col=RED, num=None)
        appear(f, moved, t, st[3] + 0.2, 0.5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- the gap ----
def build_gap(T, st, sents):
    base = shell("The gap"); tl = title("Governed, but checked against itself", "Version 2.1 reconciled against a table in the same database")
    # left panel: one database
    L1 = card(CX0, 214, 820, 560, r=20, accent=RED); s = SS(820, 560)
    s.text((34, 30), "Before: reconcile inside one database", 28, INK, bold=True)
    s.rr((40, 100, 780, 420), 18, fill=(240, 244, 251), outline=LINE, width=2); s.text((64, 116), "SAP HANA  ·  one HDI container", 22, MUTE, bold=True)
    for x0, ttl, sub in ((70, "Stock tables", "what the service reads"), (440, "SystemOfRecord", "a table in the same DB")):
        s.rr((x0, 170, x0 + 300, 300), 14, fill=WHITE, outline=AZURE, width=2); s.text((x0 + 22, 192), ttl, 24, INK, bold=True); s.text((x0 + 22, 232), sub, 19, MUTE)
    s.line([(372, 235), (438, 235)], AZURE, 4); s.poly([(438, 235), (426, 228), (426, 242)], AZURE); s.poly([(372, 235), (384, 228), (384, 242)], AZURE)
    s.text((410, 350), "agree", 22, AZURE, bold=True, anchor="mm")
    L1.im.alpha_composite(s.done(), (26, 26))
    bad = chip(CX0 + 40, 214 + 455, "Same source, same blind spot: agreement proves little", 22, fg=RED, bg=PALERED, outline=RED)
    # right panel: independent ledger
    R1 = card(1010, 214, 860, 560, r=20, accent=GREEN); r = SS(860, 560)
    r.text((34, 30), "Now: an independent ledger", 28, INK, bold=True)
    r.rr((40, 110, 360, 250), 14, fill=WHITE, outline=AZURE, width=2); r.text((62, 132), "Stock service", 24, INK, bold=True); r.text((62, 172), "reads SAP HANA,", 19, MUTE); r.text((62, 198), "computes in code", 19, MUTE)
    r.rr((500, 110, 820, 250), 14, fill=PALEACC, outline=ACC, width=2); r.text((522, 132), "sap-gov-ledger", 24, INK, bold=True); r.text((522, 172), "separate app, own data,", 19, MUTE); r.text((522, 198), "own token check", 19, MUTE)
    r.rr((40, 330, 820, 420), 14, fill=(244, 247, 252), outline=LINE, width=2); r.text((62, 352), "Reached only through the Destination service", 22, INK, bold=True)
    r.text((62, 386), "GovLedgerService  ·  OAuth token with scope agent", 19, MUTE)
    R1.im.alpha_composite(r.done(), (26, 26))
    arr, _ = arrow_layer([(1010 + 362, 214 + 180), (1010 + 498, 214 + 180)], ACC, 5)
    good = chip(1050, 214 + 455, "A second, independent source for the same figure", 22, fg=GREEN, bg=PALEGREEN, outline=GREEN)

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        appear(f, L1, t, st[0] + 0.2, 0.6); appear(f, bad, t, st[1] + 0.4)
        appear(f, R1, t, st[2] + 0.2, 0.6); appear(f, arr, t, st[2] + 1.0, 0.4, slide=0); appear(f, good, t, st[2] + 1.8)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- workflow ----
WHO = {"LLM": (AZURE, PALE, AZURE), "SAP service": (INDIGO, (234, 232, 250), VIOLET), "Ledger": ((0, 110, 118), PALEACC, ACC)}
STEPS = [("1", "Ask", "LLM", "User asks in plain language", ["Is order 1000001", "ready?"]),
         ("2", "Choose a tool", "LLM", "Model picks one governed function", ["validateOrder", "Stock(1000001)"]),
         ("3", "Look up", "SAP service", "Reads order, components and stock on SAP HANA", ["SELECT … on", "SAP HANA"]),
         ("4", "Compute", "SAP service", "Sums stock per material in code", ["8.8 available", "vs 10 required"]),
         ("5", "Cross-check", "Ledger", "Same figure from the independent ledger, via destination", ["ledger: 8.8", "(or 9.1)"]),
         ("6", "Answer", "LLM", "Model phrases the result and any mismatch", ["MATCH or", "MISMATCH"]),
         ("7", "Audit row", "SAP service", "One chained row: tool, outcome, status, conversation", ["OK · 200", "seq 11"])]


def build_workflow(T, st, sents):
    base = shell("Workflow"); tl = title("One question, seven steps, three roles", "The model talks. The SAP service computes. The ledger cross-checks.")
    CW, GAP = 226, 23; cards, exs = [], []
    for i, (n, ttl, who, desc, ex) in enumerate(STEPS):
        x = CX0 + i * (CW + GAP); fg, pale, acc = WHO[who]
        c = card(x, 212, CW, 330, r=18, accent=acc); s = SS(CW, 330)
        s.ellipse((24, 26, 72, 74), fill=acc); s.text((48, 51), n, 26, WHITE, bold=True, anchor="mm")
        s.text((24, 92), ttl, 26, INK, bold=True)
        for j, l in enumerate(wrap(desc, 20, CW - 44)[:4]): s.text((24, 136 + j * 27), l, 20, MUTE)
        s.rr((20, 272, CW - 20, 312), 20, fill=pale, outline=acc, width=2); s.text((CW / 2, 292), who, 20, fg, bold=True, anchor="mm")
        c.im.alpha_composite(s.done(), (26, 26)); cards.append(c)
        e = card(x, 580, CW, 92, r=14, fill=(248, 250, 255)); es = SS(CW, 92)
        for j, l in enumerate(ex): es.text((CW / 2, 14 + j * 34), l, 19, INK, bold=True, mono=True, anchor="ma")
        e.im.alpha_composite(es.done(), (26, 26)); exs.append(e)
    arrows = [arrow_layer([(CX0 + i * (CW + GAP) + CW + 2, 377), (CX0 + (i + 1) * (CW + GAP) - 2, 377)], MUTE, 3, head=9)[0] for i in range(6)]
    legend = [chip(CX0, 712, "LLM: understands the question and phrases the answer. Never calculates.", 23, fg=AZURE, bg=PALE, outline=AZURE),
              chip(CX0, 770, "SAP service: looks up, computes in code, records every call.", 23, fg=INDIGO, bg=(234, 232, 250), outline=VIOLET),
              chip(CX0, 828, "Ledger: a second, independent source for the same figure.", 23, fg=(0, 110, 118), bg=PALEACC, outline=ACC)]
    tt = [st[0] + 0.5, st[1] + 0.2, st[1] + 1.8, st[1] + 3.4, st[2] + 0.2, st[3] + 0.2, st[4] + 0.2]

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        for i in range(7):
            appear(f, cards[i], t, tt[i], 0.5); appear(f, exs[i], t, tt[i] + 0.3)
            if i < 6: appear(f, arrows[i], t, tt[i] + 0.4, 0.3, slide=0)
        act = max([i for i in range(7) if t >= tt[i]] or [0])
        if t >= tt[0]:
            x = CX0 + act * (CW + GAP); ImageDraw.Draw(f).rounded_rectangle((x + 10, 552, x + CW - 10, 560), 4, fill=ACC)
        appear(f, legend[0], t, st[1] + 0.6); appear(f, legend[1], t, st[1] + 2.4); appear(f, legend[2], t, st[2] + 0.8)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- architecture ----
def build_arch(T, st, sents):
    base = shell("Architecture"); tl = title("Architecture on SAP BTP")
    cont = SS(1400, 712); cont.rr((2, 2, 1398, 710), 24, fill=(236, 244, 255, 255), outline=AZURE, width=3)
    cont.text((26, 14), "SAP BTP  ·  Cloud Foundry (trial subaccount, US East)", 22, AZURE, bold=True); cont = L(cont.done(), 470, 196)
    N = dict(user=node(150, 265, 420, 375, "Browser", "chat UI with sign-in", ACC, ic="chat"),
             llm=node(150, 525, 420, 635, "LLM API", "non-SAP · sees tool results only", MUTE, fill=(248, 248, 250), dashed=True),
             agent=node(520, 265, 830, 375, "sap-gov-agent", "chat app · holds the tool loop", AZURE, ic="gear"),
             dest=node(1010, 265, 1320, 375, "Destination service", "GovStockService · GovLedgerService", AZURE, ic="cloud"),
             xs=node(1500, 265, 1830, 375, "XSUAA", "OAuth tokens · scope agent", VIOLET, ic="shield"),
             cap=node(520, 525, 830, 635, "CAP stock service", "governed functions + reconcile", AZURE, ic="gear"),
             ledger=node(1500, 525, 1830, 635, "sap-gov-ledger", "separate app · own token check", ACC, ic="book", badge="NEW"),
             hana=node(520, 770, 830, 880, "SAP HANA Cloud", "orders · stock · chained AuditLog", GREEN, ic="db"),
             ldata=node(1500, 770, 1830, 880, "Ledger data", "its own balances, not HANA", ACC, ic="db"))
    E = [("ask", [(420, 320), (520, 320)], ACC, None, (470, 296)),
         ("prompt + tools", [(570, 375), (570, 450), (285, 450), (285, 525)], MUTE, (8, 6), (400, 426)),
         ("get token", [(830, 320), (1010, 320)], AZURE, None, (920, 296)),
         ("OAuth 2.0", [(1320, 320), (1500, 320)], VIOLET, None, (1410, 296)),
         ("call + token + conv id", [(675, 375), (675, 525)], AZURE, None, (600, 482)),
         ("token for GovLedgerService", [(800, 525), (800, 455), (1165, 455), (1165, 375)], ACC, None, (1000, 432)),
         ("GET balances via destination", [(830, 580), (1500, 580)], ACC, None, (1165, 556)),
         ("validate token", [(1665, 525), (1665, 375)], VIOLET, None, (1572, 450)),
         ("SQL + chained audit row", [(675, 635), (675, 770)], GREEN, None, (820, 702)),
         ("own data", [(1665, 635), (1665, 770)], ACC, None, (1752, 702))]
    els = []
    for lab, pts, col, dash, lp in E:
        lay, ln = arrow_layer(pts, col, 4, dash=dash, head=12); w_ = tw(lab, 18, True) + 22
        els.append((lab, pts, lay, ln, col, chip(lp[0] - w_ / 2, lp[1] - 16, lab, 18, fg=INK, bg=WHITE, outline=col, padx=11, pady=3)))
    noacc = chip(1005, 805, "no access to the stock database", 19, fg=RED, bg=PALERED, outline=RED, padx=12, pady=4)
    sched = {"ledger": st[0] + 0.3, "dest": st[0] + 1.0, "ldata": st[0] + 1.7, "agent": st[1] + 0.2, "user": st[1] + 0.2, "cap": st[1] + 1.2, "xs": st[1] + 2.4,
             "hana": st[2] + 0.2, "llm": st[3] + 0.2}
    et = [st[1] + 0.6, st[3] + 0.6, st[1] + 0.9, st[1] + 2.7, st[1] + 1.6, st[1] + 3.2, st[2] + 1.6, st[2] + 2.4, st[2] + 0.6, st[2] + 3.0]

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]; appear(f, cont, t, 0.3, 0.6, slide=0)
        for k, lay in N.items(): appear(f, lay, t, sched[k], 0.5)
        for (lab, pts, lay, ln, col, badge), t0 in zip(els, et):
            p = prog(t, t0, 0.7)
            if p <= 0: continue
            blit(f, lay, clip=reveal_clip(lay, pts, ease_io(p)) if p < 1 else None)
            if p >= 1:
                appear(f, badge, t, t0 + 0.7, 0.3, slide=10)
                d = ((t - t0 - 0.7) * 240) % (ln + 80)
                if d <= ln: paste_dot(f, path_point(pts, d), col, 6)
        appear(f, noacc, t, st[2] + 3.6, 0.4)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- built live ----
def build_built(T, st, sents):
    base = shell("Built live"); tl = title("Built live on a personal SAP BTP trial", "Real screens from today's run, 18 October 2026")
    apps, sa, oa = shot_card("cf_apps_v22", CX0, 215, 1060, crop=(250, 90, 1545, 420))
    dest, sd, od = shot_card("destinations_v22", 1250, 215, 620, crop=(690, 120, 1560, 400))
    la = chip(CX0, 215 + apps.h - 26, "Four Cloud Foundry apps in space dev", 22, fg=AZURE, bg=PALE, outline=AZURE)
    ld = chip(1250, 215 + dest.h - 26, "GovLedgerService next to GovStockService", 21, fg=(0, 110, 118), bg=PALEACC, outline=ACC)
    term, stt, ot = shot_card("bas_destsetup_baseline", CX0, 690, 1720, crop=(0, 0, 1378, 23))
    lt = chip(CX0, 636, "Created by a one-off task inside the platform (cf run-task): no secret typed or shown", 21, fg=INDIGO, bg=(234, 232, 250), outline=VIOLET)

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        appear(f, apps, t, st[0] + 0.3, 0.6); appear(f, la, t, st[0] + 1.0)
        callout(f, t, st[0] + 2.2, (262, 274, 1530, 304), sa, oa, crop0=(250, 90), col=ACC)
        appear(f, dest, t, st[1] + 0.2, 0.6); appear(f, ld, t, st[1] + 0.9)
        callout(f, t, st[1] + 1.6, (704, 262, 1545, 288), sd, od, crop0=(690, 120), col=ACC)
        appear(f, lt, t, st[2] + 0.1); appear(f, term, t, st[2] + 0.4, 0.6)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- live: match ----
def side_card(x, y, w, n, ttl, lines, col):
    h = 70 + len(lines) * 32 + 18; c = card(x, y, w, h, r=16, accent=col); s = SS(w, h)
    s.ellipse((26, 22, 70, 66), fill=col); s.text((48, 44), n, 24, WHITE, bold=True, anchor="mm"); s.text((86, 30), ttl, 26, INK, bold=True)
    for j, l in enumerate(lines): s.text((28, 84 + j * 32), l, 22, MUTE)
    c.im.alpha_composite(s.done(), (26, 26)); return c


def build_match(T, st, sents):
    base = shell("Live: match"); tl = title("The live agent on SAP BTP", "sap-gov-agent.cfapps.us10-001.hana.ondemand.com  ·  18 October 2026")
    shotc, sc, org = shot_card("chat_match", CX0, 210, 1010)
    c1 = side_card(1250, 210, 620, "1", "Numbers from the tool", ["material 42: required 10,", "available 8.8, short by 1.2.", "Nothing estimated by the model."], AZURE)
    c2 = side_card(1250, 446, 620, "2", "Cross-checked: MATCH", ["The ledger, reached through", "GovLedgerService, agrees."], GREEN)
    c3 = side_card(1250, 650, 620, "3", "One id, end to end", ["The conversation id goes to the", "service and into the audit row."], ACC)

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        appear(f, shotc, t, st[0] + 0.2, 0.6)
        callout(f, t, st[1] + 0.4, (30, 287, 640, 307), sc, org, col=AZURE, num=1); appear(f, c1, t, st[1] + 0.6)
        callout(f, t, st[2] + 0.2, (30, 330, 622, 352), sc, org, col=GREEN, num=2); appear(f, c2, t, st[2] + 0.4)
        callout(f, t, st[2] + 2.4, (30, 380, 440, 396), sc, org, col=ACC, num=3); appear(f, c3, t, st[2] + 2.6)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- live: mismatch ----
def num_tile(x, y, w, head, val, col, pale):
    c = card(x, y, w, 186, r=18, fill=pale, outline=col); s = SS(w, 186)
    s.text((26, 22), head, 21, MUTE, bold=True); s.text((26, 58), val, 88, col, bold=True)
    c.im.alpha_composite(s.done(), (26, 26)); return c


def build_mismatch(T, st, sents):
    base = shell("Live: mismatch"); tl = title("Change one number in the ledger", "Same question, same agent: does it notice?")
    cmd = mono_card(CX0, 206, 1720, [("$ cf set-env sap-gov-ledger LEDGER_ADJUST '{\"42\":9.1}'  &&  cf restart sap-gov-ledger", (225, 235, 255))], size=22, head="BAS terminal")
    shotc, sc, org = shot_card("chat_mismatch", CX0, 352, 880)
    a = num_tile(1090, 352, 380, "STOCK SERVICE · SAP HANA", "8.8", INK, WHITE)
    b = num_tile(1490, 352, 380, "INDEPENDENT LEDGER", "9.1", (180, 100, 0), PALEAMB)
    mm = chip(1090, 572, "MISMATCH: material 42, 8.8 vs 9.1", 27, fg=WHITE, bg=RED, padx=24, pady=10)
    rest = mono_card(1090, 660, 780, [("$ cf unset-env sap-gov-ledger LEDGER_ADJUST", (225, 235, 255)), ("$ cf restart sap-gov-ledger", (225, 235, 255))], size=20)
    ok = chip(1090, 790, "Next answer: MATCH again", 25, fg=GREEN, bg=PALEGREEN, outline=GREEN)

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        appear(f, cmd, t, st[0] + 0.3, 0.6)
        appear(f, shotc, t, st[1] + 0.1, 0.6); appear(f, a, t, st[1] + 0.8); appear(f, b, t, st[1] + 1.4)
        callout(f, t, st[1] + 3.0, (30, 330, 735, 372), sc, org, col=RED, width=5); pop(f, mm, t, st[1] + 3.4, 0.5)
        callout(f, t, st[2] + 0.3, (30, 287, 640, 307), sc, org, col=AZURE)
        appear(f, rest, t, st[3] + 0.2, 0.5); appear(f, ok, t, st[3] + 1.2)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- sequence ----
def _head(x, ttl, sub, col, w=214):
    c = card(x - w // 2, 200, w, 74, r=14, accent=col); s = SS(w, 74); s.text((w / 2, 18), ttl, 21, INK, bold=True, anchor="ma"); s.text((w / 2, 46), sub, 16, MUTE, anchor="ma")
    c.im.alpha_composite(s.done(), (26, 26)); return c


def build_sequence(T, st, sents):
    base = shell("Sequence"); tl = title("One question, end to end")
    LL = [("User", "browser", ACC), ("Chat app", "sap-gov-agent", AZURE), ("LLM", "non-SAP", MUTE), ("CAP service", "/stock", INDIGO),
          ("Destination", "service", VIOLET), ("Ledger", "sap-gov-ledger", ACC), ("SAP HANA", "data + AuditLog", GREEN)]
    X = [CX0 + 110 + i * 250 for i in range(7)]; heads = [_head(X[i], *LL[i]) for i in range(7)]
    life = SS(W, H, k=1)
    for x in X: life.line([(x, 290), (x, 900)], (190, 202, 222, 255), 3, dash=(10, 8))
    life = L(life.done(), 0, 0)
    M = [(0, 1, "1  Is order 1000001 ready?", ACC, False), (1, 2, "2  question + tool list", AZURE, False), (2, 1, "3  call validateOrderStock", MUTE, True),
         (1, 4, "4  token for GovStockService", VIOLET, False), (1, 3, "5  GET validateOrderStock + conversation id", AZURE, False),
         (3, 6, "6  read order, components, stock", GREEN, False), ("note", 3, "7  verdict computed in code", AMBER, False),
         (3, 4, "8  token for GovLedgerService", VIOLET, False), (3, 5, "9  GET balances (scope agent)", ACC, False), (5, 3, "10  ledger figure", ACC, True),
         (3, 6, "11  INSERT chained AuditLog row (MATCH / MISMATCH)", GREEN, False), (3, 1, "12  verdict + both figures", AZURE, True), (1, 0, "13  answer, via the model", AZURE, True)]
    Y0, DY = 316, 45
    groups = [(1, 0, 7), (2, 7, 10), (3, 10, 13)]; times = [0.0] * 13
    for si, a_, b_ in groups:
        nxt = st[si + 1] if si + 1 < len(st) else T - 0.8; span = max(1.0, nxt - st[si] - 0.4)
        for k in range(a_, b_): times[k] = st[si] + 0.15 + (k - a_) * span / (b_ - a_)
    els = []
    for k, (a_, b_, txt, col, ret) in enumerate(M):
        y = Y0 + k * DY
        if a_ == "note":
            els.append((k, None, label(X[b_] - 150, y, txt, 18, fg=(140, 80, 0), bg=PALEAMB, outline=AMBER), None, y, col)); continue
        x1 = X[a_] + (10 if b_ > a_ else -10); x2 = X[b_] - (10 if b_ > a_ else -10)
        arr, _ = arrow_layer([(x1, y), (x2, y)], col, 4, dash=(9, 6) if ret else None, head=12)
        els.append((k, arr, label((x1 + x2) / 2, y - 18, txt, 17), ((x1, y), (x2, y)), y, col))

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        for i, h in enumerate(heads): appear(f, h, t, 0.25 + i * 0.12, 0.4)
        blit(f, life, a=prog(t, 0.6, 0.5)); d = ImageDraw.Draw(f)
        for xi, a0, a1, col in ((1, 0, 12, AZURE), (3, 4, 11, INDIGO)):
            if t >= times[a0]:
                top = Y0 + a0 * DY - 10; full = Y0 + a1 * DY + 12
                bot = full if t >= times[a1] else top + 6 + (full - top - 6) * prog(t, times[a0], max(0.1, times[a1] - times[a0]))
                d.rounded_rectangle((X[xi] - 8, top, X[xi] + 8, max(top + 6, bot)), 4, fill=mix(WHITE, col, 0.18), outline=col, width=2)
        cur = max([i for i in range(13) if times[i] <= t] or [-1])
        for k, arr, lab, pts, y, col in els:
            p = prog(t, times[k], 0.45)
            if p <= 0: continue
            if arr is None: appear(f, lab, t, times[k], 0.4); continue
            w_ = max(2, int(arr.w * ease_io(p)))
            blit(f, arr, clip=(0, 0, w_, arr.h) if pts[0][0] < pts[1][0] else (arr.w - w_, 0, arr.w, arr.h))
            if p > 0.5: appear(f, lab, t, times[k] + 0.2, 0.3, slide=8)
            if k == cur and p >= 1: d.ellipse((min(pts[0][0], pts[1][0]) - 30, y - 7, min(pts[0][0], pts[1][0]) - 16, y + 7), fill=ACC)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- legacy baseline ----
def block(x, y, w, h, ttl, lines, col, fill=WHITE):
    c = card(x, y, w, h, r=14, fill=fill, outline=col, accent=col); s = SS(w, h); s.text((20, 22), ttl, 23, INK, bold=True)
    for j, l in enumerate(lines): s.text((20, 60 + j * 28), l, 20, MUTE)
    c.im.alpha_composite(s.done(), (26, 26)); return c


def build_baseline(T, st, sents):
    base = shell("Legacy rows"); tl = title("Sealing the rows written before the chain", "A one-time baseline, then the chain verifies end to end")
    B = [block(CX0, 214, 270, 140, "seq 1 – 8", ["chained rows", "prevHash → hash"], AZURE),
         block(CX0 + 330, 214, 330, 140, "seq 9 · baseline", ["attests 21 legacy rows", "digest 6cee364f…"], ACC, fill=PALEACC),
         block(CX0 + 720, 214, 250, 140, "seq 10", ["chained row", "prevHash → hash"], AZURE),
         block(CX0 + 1030, 214, 270, 140, "seq 11 · head", ["head hash", "50a253e8f4f7…"], AZURE)]
    links = [arrow_layer([(CX0 + 272, 284), (CX0 + 328, 284)], AZURE, 4, head=11)[0], arrow_layer([(CX0 + 662, 284), (CX0 + 718, 284)], AZURE, 4, head=11)[0],
             arrow_layer([(CX0 + 972, 284), (CX0 + 1028, 284)], AZURE, 4, head=11)[0]]
    stack = []
    for k in range(3):
        c = card(CX0 + 340 + k * 10, 470 - k * 10, 310, 110, r=12, fill=(246, 247, 250), outline=LINE, shadow=k == 2); stack.append(c)
    s = SS(310, 110); s.text((20, 18), "21 legacy rows", 24, INK, bold=True); s.text((20, 56), "written before the chain", 19, MUTE); stack[-1].im.alpha_composite(s.done(), (26, 26))
    seal, _ = arrow_layer([(CX0 + 505, 448), (CX0 + 505, 360)], ACC, 5, head=13)
    seal_l = chip(CX0 + 530, 392, "digest sealed into seq 9", 19, fg=(0, 110, 118), bg=PALEACC, outline=ACC, padx=12, pady=4)
    res = mono_card(1370, 440, 500, ["BASELINE (cf run-task)", ("legacyRows   21", (150, 240, 220)), ("backfilled   6 rows", (150, 240, 220)),
                                     ("attestation  seq 9", (150, 240, 220))], size=21, head="task log")
    edit = chip(CX0 + 690, 520, "edit any of the 21 later  →  verify fails", 22, fg=RED, bg=PALERED, outline=RED)
    shotc, sc, org = shot_card("bas_chain_verify", CX0, 690, 1720, crop=(0, 0, 1378, 92))
    lshot = chip(CX0, 640, "Live check today: ok true · 11 rows · legacyBaseline covered", 22, fg=GREEN, bg=PALEGREEN, outline=GREEN)

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        for k, c in enumerate(stack): appear(f, c, t, st[0] + 0.3 + k * 0.15, 0.5)
        appear(f, B[0], t, st[1] + 0.2); appear(f, links[0], t, st[1] + 0.6, 0.3, slide=0); appear(f, B[1], t, st[1] + 0.9)
        p = prog(t, st[1] + 1.8, 0.6)
        if p > 0: blit(f, seal, clip=(0, seal.h - max(2, int(seal.h * ease_io(p))), seal.w, seal.h))
        appear(f, seal_l, t, st[1] + 2.4); appear(f, res, t, st[1] + 3.0, 0.5)
        appear(f, links[1], t, st[2] + 0.2, 0.3, slide=0); appear(f, B[2], t, st[2] + 0.4); appear(f, links[2], t, st[2] + 0.8, 0.3, slide=0); appear(f, B[3], t, st[2] + 1.0)
        appear(f, lshot, t, st[2] + 1.6); appear(f, shotc, t, st[2] + 1.9, 0.6)
        callout(f, t, st[2] + 3.0, (0, 60, 1378, 92), sc, org, col=GREEN)
        pop(f, edit, t, st[3] + 0.3, 0.5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- offline verify ----
def build_verify(T, st, sents):
    base = shell("Verify"); tl = title("Export the trail, verify it anywhere", "tools/verify-export.js in the repo: plain Node, no SAP system needed")
    doc = card(CX0, 220, 640, 470, r=16, accent=AZURE); s = SS(640, 470)
    s.text((30, 26), "audit-export.jsonl", 28, INK, bold=True); s.text((30, 66), "one header line, then one line per row", 20, MUTE)
    rows = ['{"type":"header",', ' "format":"gov-audit-export/1",', ' "rows":N, "headSeq":N, ...}', '{"type":"row","seq":1,', ' "prevHash":"…","hash":"…"}', '{"type":"row","seq":2, ...}', '…']
    for j, l in enumerate(rows): s.text((30, 116 + j * 44), l, 21, TEXT, mono=True)
    doc.im.alpha_composite(s.done(), (26, 26))
    arr, _ = arrow_layer([(CX0 + 660, 455), (CX0 + 760, 455)], ACC, 5)
    term = mono_card(CX0 + 780, 220, 940, ["$ node tools/verify-export.js audit-export.jsonl", "",
                                           ("OK  <rows> rows, seq 1..<n>, anchored at genesis,", (150, 240, 200)), ("    head <hash>", (150, 240, 200))], size=22, head="any machine with Node")
    term2 = mono_card(CX0 + 780, 500, 940, ["# after someone edits row 7:", ("BROKEN at seq 7: row content does not match its hash", (255, 140, 150))], size=22)
    note = chip(CX0 + 780, 690, "Shown: the verifier's output format (exit 0 = intact, 1 = broken)", 20, fg=MUTE, bg=WHITE, outline=LINE, bold=False)

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        appear(f, doc, t, st[0] + 0.3, 0.6); appear(f, arr, t, st[0] + 1.2, 0.4, slide=0); appear(f, term, t, st[0] + 1.6, 0.6)
        appear(f, term2, t, st[1] + 0.6, 0.5); appear(f, note, t, st[1] + 1.6)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- difference ----
ROWS = [("Ask", "Navigate transactions or apps: order, then components, then stock", "Ask in plain language: “Is order 1000001 ready?”"),
        ("Cross-check", "Compare screens or reports by eye, if anyone checks at all", "The service asks an independent ledger on every answer and flags a mismatch"),
        ("Where logic lives", "In transactions and individual judgment", "In one versioned, unit-tested service function per question"),
        ("Audit trail", "Change documents and logs, not tied to the question asked", "One chained row per call, exportable and verifiable offline"),
        ("Extending", "Custom development and transports", "Add a function and a tool definition, redeploy the MTA")]


def build_difference(T, st, sents):
    base = shell("Difference"); tl = title("How is this different from conventional SAP?")
    X1, X2, X3, RW, RH, Y0 = CX0, CX0 + 300, CX0 + 1010, 1720, 96, 226
    h1 = chip(X2, 166, "Conventional SAP", 26, fg=WHITE, bg=SLATE); h2 = chip(X3, 166, "Governed SAP agents", 26, fg=WHITE, bg=AZURE)
    rows = []
    for i, (lab, a, b) in enumerate(ROWS):
        y = Y0 + i * (RH + 10); c = card(X1, y, RW, RH, r=14); s = SS(RW, RH)
        s.text((24, RH / 2), lab, 24, (0, 110, 118), bold=True, anchor="lm"); s.line([(X2 - X1 - 22, 14), (X2 - X1 - 22, RH - 14)], LINE, 2); s.line([(X3 - X1 - 22, 14), (X3 - X1 - 22, RH - 14)], LINE, 2)
        c.im.alpha_composite(s.done(), (26, 26))
        def txt(x, t_, col, wd):
            ls = wrap(t_, 23, wd); return text_layer(x, y + RH / 2 - len(ls) * 15, ls, 23, col, gap=1.25)
        rows.append((c, txt(X2, a, TEXT, 670), txt(X3, b, INK, 690)))
    band = card(X1, Y0 + 5 * (RH + 10) + 6, RW, 66, r=14, fill=PALEGREEN, outline=GREEN, accent=GREEN); sb = SS(RW, 66)
    sb.text((30, 34), "Unchanged:  SAP HANA  ·  SAP BTP  ·  the SAP security model (OAuth, XSUAA)  ·  your SAP data", 25, GREEN, bold=True, anchor="lm"); band.im.alpha_composite(sb.done(), (26, 26))

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        appear(f, h1, t, st[1] - 0.1, 0.4); appear(f, h2, t, st[2] - 0.1, 0.4)
        sp1 = (st[2] - st[1]) * 0.8 / 5; sp2 = (st[3] - st[2]) * 0.8 / 5
        for i, (c, a, b) in enumerate(rows):
            appear(f, c, t, st[0] + 0.4 + i * 0.2, 0.4); appear(f, a, t, st[1] + 0.4 + i * sp1, 0.45); appear(f, b, t, st[2] + 0.4 + i * sp2, 0.45)
        appear(f, band, t, st[3] + 0.2, 0.5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- limits ----
def build_limits(T, st, sents):
    base = shell("Limits"); tl = title("Honest limits, and what comes next")
    specs = [(AMBER, "1", "A stand-in ledger", ["The ledger is a second app", "with sample data. In production", "it would be a real system of", "record, such as S/4HANA."], st[1]),
             (RED, "2", "Trust boundaries", ["The end-user name is asserted", "by the caller, not authenticated.", "The chain detects tampering;", "it does not prevent it."], st[2]),
             (GREEN, ">", "Next", ["A real SAP API behind the", "destination. HANA audit", "policies or an external anchor.", "A model inside your approved", "boundary."], st[3])]
    cards = []
    for i, (col, n, ttl, ls_, t0) in enumerate(specs):
        x = CX0 + i * 587; c = card(x, 214, 546, 470, r=20, accent=col); s = SS(546, 470)
        s.ellipse((32, 34, 96, 98), fill=col); s.text((64, 66), n, 32, WHITE, bold=True, anchor="mm"); s.text((32, 128), ttl, 31, INK, bold=True)
        for j, l in enumerate(ls_): s.text((32, 190 + j * 44), l, 25, TEXT)
        c.im.alpha_composite(s.done(), (26, 26)); cards.append((c, t0))
    model = chip(CX0, 730, "The language model is not an SAP model: regulated data needs an approved one.", 23, fg=INDIGO, bg=(234, 232, 250), outline=VIOLET)

    def draw(f, t):
        f.paste(base, (0, 0)); [appear(f, l, t, 0.15) for l in tl]
        for c, t0 in cards: appear(f, c, t, t0 + 0.1, 0.5)
        appear(f, model, t, st[3] + 2.5)
        draw_caption(f, t, st, sents)
    return draw


# ---------------------------------------------------------------- about ----
def build_about(T, st, sents):
    bg = split_bg()
    c = card(120, 200, 980, 560, r=26, accent=AZURE); s = SS(980, 560)
    s.ellipse((50, 60, 230, 240), fill=AZURE); s.text((140, 150), "YA", 70, WHITE, bold=True, anchor="mm")
    s.text((270, 72), "Yuvaraj Aravindan", 58, INK, bold=True); s.text((272, 150), "Founder, AI Agentic Enterprises", 32, AZURE, bold=True)
    s.text((272, 214), "Governed AI agents for regulated industries,", 27, TEXT); s.text((272, 252), "on enterprise platforms like SAP.", 27, TEXT)
    s.text((272, 330), "ai-agentic-enterprises.com", 36, (0, 110, 118), bold=True)
    c.im.alpha_composite(s.done(), (26, 26))
    chips, cx = [], 172
    for txt_, fg_, bg_, ol_ in (("Enterprise applications", AZURE, PALE, AZURE), ("AI agents & governance", (0, 110, 118), PALEACC, ACC), ("SAP BTP · HANA", INDIGO, (234, 232, 250), VIOLET)):
        ch_ = chip(cx, 640, txt_, 23, fg=fg_, bg=bg_, outline=ol_); chips.append(ch_); cx += ch_.w + 8
    a_im, sw = big_chip("SAP", 96, WHITE, AZURE); b_im, aw = big_chip("Agents", 96, ACC, WHITE)
    chip_sap = L(a_im, 1290 - 30, 300 - 30); chip_ag = L(b_im, 1290 - 30, 470 - 30)
    tag = text_layer(1292, 650, ["Part 2: when two systems", "disagree, the agent says so."], 32, WHITE, bold=True)
    note = text_layer(122, 800, "Independent demonstration on an SAP BTP trial account. Not an SAP product announcement.", 24, MUTE)

    def draw(f, t):
        f.paste(bg, (0, 0)); appear(f, c, t, 0.3, 0.6)
        for i, ch in enumerate(chips): appear(f, ch, t, st[0] + 1.6 + i * 0.4, 0.4)
        pop(f, chip_sap, t, 0.6); pop(f, chip_ag, t, 1.0); appear(f, tag, t, 1.6)
        appear(f, note, t, st[1] + 0.2, 0.6)
        draw_caption(f, t, st, sents)
    return draw


BUILD = {"banner": build_banner, "recap": build_recap, "gap": build_gap, "workflow": build_workflow, "architecture": build_arch, "built": build_built,
         "match": build_match, "mismatch": build_mismatch, "sequence": build_sequence, "baseline": build_baseline, "verify": build_verify,
         "difference": build_difference, "limits": build_limits, "about": build_about}
