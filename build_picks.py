"""Pagini statice pentru Google, una pentru fiecare Pick of the Day (RO, EN, DE), plus arhiva pick-urilor:
  /ro/pick/sp500-vanzare-2026-11-23.html   /en/pick/sp500-sell-2026-11-23.html   /de/pick/sp500-verkaufen-2026-11-23.html
  /ro/pick/   /en/pick/   /de/pick/
Datele vin din tabelul public daily_picks (inclusiv graficul: chart + after). Apelat din build_pages.py."""
from __future__ import annotations

import html
from datetime import date

import pick_visual as pv

LANGS = ("ro", "en", "de")
SLUG = {"WTI": ("petrol-wti", "oil-wti", "oel-wti"), "GOLD": ("aur", "gold", "gold"), "SILVER": ("argint", "silver", "silber")}
NAME = {
    "ro": {"WTI": "Petrol (WTI)", "GOLD": "Aur", "SILVER": "Argint"},
    "en": {"WTI": "Oil (WTI)", "GOLD": "Gold", "SILVER": "Silver"},
    "de": {"WTI": "Öl (WTI)", "GOLD": "Gold", "SILVER": "Silber"},
}
LABEL = {"EURUSD": "EUR/USD", "GBPUSD": "GBP/USD", "USDJPY": "USD/JPY", "NVIDIA": "Nvidia", "GOOGLE": "Google", "MICROSOFT": "Microsoft",
         "C3AI": "C3.ai", "INFINEON": "Infineon"}
MON = {"ro": ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"],
       "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
       "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]}
DAYS = {"ro": ["luni", "marți", "miercuri", "joi", "vineri", "sâmbătă", "duminică"],
        "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "de": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]}

T = {
    "ro": dict(buy="cumpărare", sell="vânzare", BUY="CUMPĂRARE", SELL="VÂNZARE", entry="Intrare (închiderea)", target="Țintă", stop="Stop",
               horizon="Orizont", days5="5 zile", why="De ce această alegere", archive="Toate pick-urile", home="/?lang=ro",
               sub="/?lang=ro&sub=1", sub_t="Primește Pick of the Day pe email, în fiecare dimineață – gratuit",
               report="Raportul complet din acea zi", prev="Pick-ul anterior", next="Pick-ul următor",
               open_t="În curs", closed_t="Încheiat", tgt_hit="ținta atinsă", stp_hit="stopul atins", time_out="închis după 5 zile",
               so_far="până la închiderea din", left1="mai are o zi", leftn="mai are {n} zile", ends="se încheie la următoarea închidere",
               not_yet="Începe la următoarea închidere.", acc="/acuratete.html", acc_t="Cât de des nimerim",
               chart_note="Linia neagră: prețul înainte de alegere. Linia aurie: ce a făcut prețul după. Zona verde: spre țintă; zona roșie: spre stop.",
               costs=("Idee educativă, nu recomandare de investiții. Rezultatele sunt fără spread, comisioane și dobânda pe noapte de la broker; "
                      "în tranzacționare reală, aceste costuri pot înghiți avantajul. Performanțele trecute nu garantează rezultate viitoare."),
               title="Pick of the Day {d}: {name} – {side}", h1="{name}: {side} · Pick of the Day, {d}",
               arch_title="Toate pick-urile zilei, cu rezultate | Daily Market", arch_h1="Pick of the Day: toate alegerile și rezultatele",
               arch_desc=("În fiecare zi de bursă alegem o singură piață, cu intrare, țintă și stop pe 5 zile. Aici sunt toate, "
                          "cu rezultatul fiecăreia – inclusiv pierderile."),
               stats="{n} pick-uri încheiate: {w} pe plus ({p}%), rezultat mediu {avg}.", col_res="Rezultat"),
    "en": dict(buy="buy", sell="sell", BUY="BUY", SELL="SELL", entry="Entry (close)", target="Target", stop="Stop", horizon="Horizon",
               days5="5 days", why="Why this pick", archive="All picks", home="/?lang=en", sub="/?lang=en&sub=1",
               sub_t="Get the Pick of the Day by email, every morning – free", report="The full report from that day",
               prev="Previous pick", next="Next pick", open_t="Open", closed_t="Closed", tgt_hit="target hit", stp_hit="stop hit",
               time_out="closed after 5 days", so_far="at the close of", left1="1 day left", leftn="{n} days left",
               ends="ends at the next close", not_yet="Starts at the next close.", acc="/accuracy.html", acc_t="How often we are right",
               chart_note="Black line: the price before the pick. Gold line: what the price did after. Green zone: towards the target; red zone: towards the stop.",
               costs=("An educational idea, not investment advice. Results exclude the broker's spread, commissions and overnight financing; "
                      "in real trading, these costs can eat up the edge. Past performance does not guarantee future results."),
               title="Pick of the Day {d}: {name} – {side}", h1="{name}: {side} · Pick of the Day, {d}",
               arch_title="Every Pick of the Day, with results | Daily Market", arch_h1="Pick of the Day: every pick and its result",
               arch_desc=("Every trading day we choose one market, with an entry, a target and a stop over 5 days. Here they all are, "
                          "with the result of each one – losses included."),
               stats="{n} closed picks: {w} positive ({p}%), average result {avg}.", col_res="Result"),
    "de": dict(buy="Kauf", sell="Verkauf", BUY="KAUFEN", SELL="VERKAUFEN", entry="Einstieg (Schluss)", target="Ziel", stop="Stopp",
               horizon="Horizont", days5="5 Tage", why="Warum dieser Pick", archive="Alle Picks", home="/?lang=de", sub="/?lang=de&sub=1",
               sub_t="Den Pick of the Day jeden Morgen per E-Mail – kostenlos", report="Der vollständige Bericht von diesem Tag",
               prev="Vorheriger Pick", next="Nächster Pick", open_t="Offen", closed_t="Abgeschlossen", tgt_hit="Ziel erreicht",
               stp_hit="Stopp erreicht", time_out="nach 5 Tagen geschlossen", so_far="zum Schluss vom", left1="noch 1 Tag", leftn="noch {n} Tage",
               ends="endet zum nächsten Schluss", not_yet="Beginnt zum nächsten Schluss.", acc="/genauigkeit.html", acc_t="Wie oft wir richtig liegen",
               chart_note="Schwarze Linie: der Kurs vor dem Pick. Goldene Linie: der Kurs danach. Grüne Zone: Richtung Ziel; rote Zone: Richtung Stopp.",
               costs=("Eine Idee zu Bildungszwecken, keine Anlageberatung. Ergebnisse ohne Spread, Kommissionen und Übernachtfinanzierung des Brokers; "
                      "im echten Handel können diese Kosten den Vorteil aufzehren. Frühere Ergebnisse sind keine Garantie für künftige."),
               title="Pick of the Day {d}: {name} – {side}", h1="{name}: {side} · Pick of the Day, {d}",
               arch_title="Alle Picks des Tages, mit Ergebnissen | Daily Market", arch_h1="Pick of the Day: alle Picks und ihre Ergebnisse",
               arch_desc=("An jedem Börsentag wählen wir einen Markt, mit Einstieg, Ziel und Stopp für 5 Tage. Hier sind alle, "
                          "mit dem Ergebnis jedes einzelnen – Verluste eingeschlossen."),
               stats="{n} abgeschlossene Picks: {w} im Plus ({p} %), durchschnittliches Ergebnis {avg}.", col_res="Ergebnis"),
}

WHY = {
    "ro": lambda up, a: [("📈" if up else "📉", f"<b>Trend pe 6 luni:</b> {'în creștere' if up else 'în scădere'}."),
                         ("✅", f"<b>Semnale tehnice:</b> tot în {'sus' if up else 'jos'}."),
                         ("🏆", "Din 14 piețe, aici cele două se potriveau cel mai clar."),
                         ("🎯", f"Ținta și stopul: cât se mișcă de obicei {a} în 5 zile."),
                         ("⛔", "Dacă prețul atinge stopul, ideea se închide cu pierdere.")],
    "en": lambda up, a: [("📈" if up else "📉", f"<b>6-month trend:</b> {'rising' if up else 'falling'}."),
                         ("✅", f"<b>Technical signals:</b> also {'up' if up else 'down'}."),
                         ("🏆", "Of 14 markets, this is where the two lined up most clearly."),
                         ("🎯", f"Target and stop: how far {a} usually moves in 5 days."),
                         ("⛔", "If the price hits the stop, the idea closes with a loss.")],
    "de": lambda up, a: [("📈" if up else "📉", f"<b>6-Monats-Trend:</b> {'steigend' if up else 'fallend'}."),
                         ("✅", f"<b>Technische Signale:</b> ebenfalls nach {'oben' if up else 'unten'}."),
                         ("🏆", "Von 14 Märkten passte beides hier am klarsten zusammen."),
                         ("🎯", f"Ziel und Stopp: so weit, wie sich {a} üblicherweise in 5 Tagen bewegt."),
                         ("⛔", "Erreicht der Kurs den Stopp, endet die Idee mit einem Verlust.")],
}

CSS = """
.pk{background:#fffbeb;border:2px solid #f59e0b;border-radius:14px;padding:14px 16px;margin:0 0 16px}
.pk .top{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.pk .nm{font-size:24px;font-weight:800}
.pk .bd{color:#fff;border-radius:999px;padding:3px 13px;font-weight:800;font-size:13px}
.pk .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px}
.pk .grid div small{display:block;font-size:12px;color:#6b7280}
.pk .grid div b{font-size:18px}
@media (max-width:520px){.pk .grid{grid-template-columns:repeat(2,1fr)}}
.st{border-radius:12px;padding:10px 12px;margin:12px 0 0;font-size:15px}
.chart{background:#fff;border-radius:12px;padding:8px;margin-top:12px}
.cn{font-size:12.5px;color:#5A6B82;margin:6px 2px 0}
.why{list-style:none;padding:0;margin:6px 0 0}
.why li{display:flex;gap:10px;padding:6px 0;font-size:15.5px}
.why li span{width:24px;flex:0 0 24px}
.note{font-size:13px;color:#5A6B82;margin-top:18px}
.pt{width:100%;border-collapse:collapse;font-size:14.5px}
.pt td{padding:9px 6px;border-bottom:1px solid #D5DCE6}
.pt a{color:#13223A;font-weight:700;text-decoration:none}
.pt .r{text-align:right;font-weight:800;white-space:nowrap}
"""


def fmt(v: float, lang: str) -> str:
    v = float(v)
    dec = 0 if abs(v) >= 1000 else 2 if abs(v) >= 10 else 4
    s = f"{v:,.{dec}f}"
    return s if lang == "en" else s.replace(",", "_").replace(".", ",").replace("_", ".")


def pct(v: float | None, lang: str) -> str:
    if v is None:
        return "–"
    s = f"{abs(v):.1f}"
    s = s if lang == "en" else s.replace(".", ",")
    return ("+" if v > 0 else "−" if v < 0 else "") + s + (" %" if lang == "de" else "%")


def long_d(d: str, lang: str) -> str:
    x = date.fromisoformat(d)
    if lang == "en":
        return f"{MON['en'][x.month - 1]} {x.day}, {x.year}"
    if lang == "de":
        return f"{x.day}. {MON['de'][x.month - 1]} {x.year}"
    return f"{x.day} {MON['ro'][x.month - 1]} {x.year}"


def short_d(d: str, lang: str) -> str:
    x = date.fromisoformat(d)
    return f"{x.month}/{x.day}" if lang == "en" else f"{x.day:02d}.{x.month:02d}" + ("." if lang == "de" else "")


def name(asset: str, lang: str) -> str:
    return NAME[lang].get(asset) or LABEL.get(asset, asset)


def path(p: dict, lang: str) -> str:
    i = LANGS.index(lang)
    a = SLUG.get(p["asset"], (p["asset"].lower(),) * 3)[i]
    side = (("cumparare", "buy", "kaufen") if int(p["side"]) > 0 else ("vanzare", "sell", "verkaufen"))[i]
    return f"/{lang}/pick/{a}-{side}-{p['day']}.html"


def live(p: dict) -> dict:
    if p.get("status") and p["status"] != "open":
        return {"open": False, "pct": float(p.get("result_pct") or 0), "status": p["status"]}
    lp = p.get("last_price")
    return {"open": True, "pct": 100 * int(p["side"]) * (float(lp) / float(p["entry"]) - 1) if lp else None,
            "left": max(int(p.get("horizon") or 5) - len(p.get("after") or []), 0), "status": "open"}


def chart_png_url(p: dict, lang: str, supabase_url: str) -> str:
    return f"{supabase_url}/storage/v1/object/public/charts/pick/{p['day']}-{lang}.png"


def status_box(p: dict, lang: str) -> str:
    t, lv = T[lang], live(p)
    if lv["open"]:
        if lv["pct"] is None:
            txt = f"<b>{t['open_t']}.</b> {t['not_yet']}"
        else:
            left = lv["left"]
            rest = t["left1"] if left == 1 else t["leftn"].format(n=left) if left else t["ends"]
            txt = f"<b>{t['open_t']}:</b> <b>{pct(lv['pct'], lang)}</b> {t['so_far']} {short_d(p['last_date'], lang)} · {rest}."
        return f'<div class="st" style="background:#f3f4f6">⏳ {txt}</div>'
    how = {"target": t["tgt_hit"], "stop": t["stp_hit"]}.get(lv["status"], t["time_out"])
    good = lv["pct"] > 0
    when = f" ({long_d(p['exit_date'], lang)})" if p.get("exit_date") else ""
    return (f'<div class="st" style="background:{"#ecfdf5" if good else "#fef2f2"};color:{"#15803d" if good else "#b91c1c"}">'
            f'{"✅" if good else "❌"} <b>{t["closed_t"]}{when}:</b> {how}, <b>{pct(lv["pct"], lang)}</b></div>')


def build_one(p: dict, lang: str, prev: dict | None, nxt: dict | None, page, report_path, has_report: set,
              supabase_url: str, root) -> tuple[str, str]:
    t = T[lang]
    up = int(p["side"]) > 0
    nm = name(p["asset"], lang)
    side = t["buy"] if up else t["sell"]
    d_long = long_d(p["day"], lang)
    title = t["title"].format(d=d_long, name=nm, side=side) + " | Daily Market"
    h1 = t["h1"].format(d=d_long, name=nm, side=side)
    lv = live(p)
    res = "" if lv["open"] else f" {t['col_res']}: {pct(lv['pct'], lang)}."
    desc = {"ro": f"{nm}, {side}: intrare {fmt(p['entry'], lang)}, țintă {fmt(p['target'], lang)}, stop {fmt(p['stop'], lang)}, pe 5 zile.{res}",
            "en": f"{nm}, {side}: entry {fmt(p['entry'], lang)}, target {fmt(p['target'], lang)}, stop {fmt(p['stop'], lang)}, over 5 days.{res}",
            "de": f"{nm}, {side}: Einstieg {fmt(p['entry'], lang)}, Ziel {fmt(p['target'], lang)}, Stopp {fmt(p['stop'], lang)}, über 5 Tage.{res}"}[lang]
    col = "#15803d" if up else "#b91c1c"
    names = {"entry": {"ro": "Intrare", "en": "Entry", "de": "Einstieg"}[lang], "target": t["target"], "stop": t["stop"],
             "next": "", "aria": h1}
    ch = p.get("chart") or {}
    svg = pv.chart_svg(list(ch.get("c") or []), float(p["entry"]), float(p["target"]), float(p["stop"]), int(p["side"]),
                       lambda v: fmt(v, lang), names, after=p.get("after") or [], horizon=int(p.get("horizon") or 5))
    chart = (f'<div class="chart">{svg}</div><p class="cn">{t["chart_note"]}</p>') if svg else ""
    art = nm if lang != "ro" else {"GOLD": "aurul", "SILVER": "argintul", "WTI": "petrolul"}.get(p["asset"], nm)
    why = "".join(f"<li><span>{ic}</span><div>{tx}</div></li>" for ic, tx in WHY[lang](up, html.escape(art)))
    rep = ""
    sd = p.get("session_date")
    if lang in ("ro", "en") and (sd, lang) in has_report:
        rep = f' · <a href="{report_path(sd, lang)}">{t["report"]}</a>'
    nav = ('<div class="pager">' + (f'<a href="{path(prev, lang)}">← {t["prev"]}: {long_d(prev["day"], lang)}</a>' if prev else "<span></span>")
           + (f'<a href="{path(nxt, lang)}">{t["next"]}: {long_d(nxt["day"], lang)} →</a>' if nxt else "") + "</div>")
    body = (f"<style>{CSS}</style><h1>{html.escape(h1)}</h1>"
            f'<div class="pk"><div class="top"><span class="nm">{html.escape(nm)}</span>'
            f'<span class="bd" style="background:{col}">{t["BUY"] if up else t["SELL"]}</span></div>'
            f'<div class="grid"><div><small>{t["entry"]}</small><b>{fmt(p["entry"], lang)}</b></div>'
            f'<div><small>{t["target"]}</small><b style="color:#15803d">{fmt(p["target"], lang)}</b></div>'
            f'<div><small>{t["stop"]}</small><b style="color:#b91c1c">{fmt(p["stop"], lang)}</b></div>'
            f'<div><small>{t["horizon"]}</small><b>{t["days5"]}</b></div></div>'
            f"{status_box(p, lang)}{chart}</div>"
            f'<h2 class="sec">{t["why"]}</h2><ul class="why">{why}</ul>'
            f'<a class="cta" href="{t["sub"]}" style="margin-top:14px">{t["sub_t"]}</a>'
            f'<p style="font-size:14px;margin:0"><a href="/{lang}/pick/">{t["archive"]}</a> · <a href="{t["acc"]}">{t["acc_t"]}</a>{rep}</p>'
            f"{nav}<p class=\"note\">{t['costs']}</p>")
    alt = {lg: path(p, lg) for lg in LANGS}
    img = chart_png_url(p, lang, supabase_url) if p.get("chart") else None
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "datePublished": p["day"],
          "dateModified": str(p.get("exit_date") or p.get("last_date") or p["day"]), "inLanguage": lang,
          "author": {"@type": "Organization", "name": "Daily Market"}, "publisher": {"@type": "Organization", "name": "Daily Market"},
          "mainEntityOfPage": f"https://dailymarketlab.com{path(p, lang)}", "image": img or "https://dailymarketlab.com/og.png"}
    out = root / path(p, lang).lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    other = path(p, "en" if lang != "en" else "ro")
    out.write_text(page(lang, path(p, lang), title, desc, body, alt, other, ld, og_image=img), encoding="utf-8")
    return path(p, lang), str(p.get("exit_date") or p.get("last_date") or p["day"])


def build_archive(picks: list[dict], lang: str, page, root) -> None:
    t = T[lang]
    done = [p for p in picks if p.get("status") and p["status"] != "open"]
    stats = ""
    if done:
        w = sum(1 for p in done if float(p.get("result_pct") or 0) > 0)
        avg = sum(float(p.get("result_pct") or 0) for p in done) / len(done)
        stats = f'<p class="lede"><b>{t["stats"].format(n=len(done), w=w, p=round(100 * w / len(done)), avg=pct(avg, lang))}</b></p>'
    rows = []
    for p in picks:
        lv = live(p)
        if lv["open"]:
            r, c = ("⏳ " + pct(lv["pct"], lang)) if lv["pct"] is not None else "⏳", "#374151"
        else:
            r, c = ("✅ " if lv["pct"] > 0 else "❌ ") + pct(lv["pct"], lang), "#15803d" if lv["pct"] > 0 else "#b91c1c"
        side = T[lang]["buy"] if int(p["side"]) > 0 else T[lang]["sell"]
        rows.append(f'<tr><td><a href="{path(p, lang)}">{html.escape(name(p["asset"], lang))} · {side}</a><br>'
                    f'<span style="color:#5A6B82;font-size:13px">{long_d(p["day"], lang)}</span></td>'
                    f'<td class="r" style="color:{c}">{r}</td></tr>')
    body = (f"<style>{CSS}</style><h1>{t['arch_h1']}</h1><p class=\"lede\">{t['arch_desc']}</p>{stats}"
            f'<a class="cta" href="{t["sub"]}">{t["sub_t"]}</a>'
            f'<table class="pt">{"".join(rows)}</table><p class="note">{t["costs"]}</p>')
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": t["arch_h1"], "description": t["arch_desc"],
          "inLanguage": lang, "url": f"https://dailymarketlab.com/{lang}/pick/"}
    out = root / lang / "pick" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(lang, f"/{lang}/pick/", t["arch_title"], t["arch_desc"], body, {lg: f"/{lg}/pick/" for lg in LANGS},
                        "/en/pick/" if lang != "en" else "/ro/pick/", ld), encoding="utf-8")


def build_all(sb, page, report_path, has_report: set, supabase_url: str, root) -> list[tuple[str, str, str, str]]:
    picks = sb("daily_picks?select=*&order=day.desc&limit=2000")
    urls = []
    for lang in LANGS:
        for i, p in enumerate(picks):
            pth, lm = build_one(p, lang, picks[i + 1] if i + 1 < len(picks) else None, picks[i - 1] if i > 0 else None,
                                page, report_path, has_report, supabase_url, root)
            urls.append((pth, lm, "weekly" if live(p)["open"] else "never", "0.7" if lang == "en" else "0.6"))
        build_archive(picks, lang, page, root)
        urls.append((f"/{lang}/pick/", date.today().isoformat(), "daily", "0.8"))
    print(f"Pick of the Day: {len(picks)} pick-uri x {len(LANGS)} limbi")
    return urls
