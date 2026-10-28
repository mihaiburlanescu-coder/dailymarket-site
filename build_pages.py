#!/usr/bin/env python3
"""
Genereaza pagini statice, citibile de Google, din rapoartele publicate in Supabase:
  /en/market-report-YYYY-MM-DD.html   /ro/raport-piete-YYYY-MM-DD.html      (raportul zilnic)
  /en/weekly/<instrument>-outlook-YYYY-MM-DD.html  /ro/weekly/<instrument>-perspectiva-YYYY-MM-DD.html
  /en/index.html  /ro/index.html  (arhive)   sitemap.xml   linkurile „Latest” din index.html
Ruleaza in GitHub Actions (vezi .github/workflows/pages.yml). Doar citire din Supabase, cu cheia publica.
Pagini noi: se genereaza doar ce lipseste + ultimele zile (care se pot actualiza).
"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://dailymarketlab.com"
SUPABASE_URL = "https://atlxahrvzhzrzfhmwwen.supabase.co"
ANON = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF0bHhhaHJ2emh6cnpmaG13d2VuIiwicm9sZSI6ImFub24i"
        "LCJpYXQiOjE3OTI0ODk2MTUsImV4cCI6MjEwODA2NTYxNX0.1lOoTQP6CYoT-qDg2oGx6EbtJP9ag2CaCxmV3Bj3DhQ")
REBUILD_LAST = 3  # ultimele rapoarte se regenereaza mereu (raportul zilei se poate republica)

MON_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MON_RO = ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie",
          "noiembrie", "decembrie"]
DAY_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAY_RO = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
ASSET_SLUG = {"SP500": ("sp500", "sp500"), "DAX": ("dax", "dax"), "VIX": ("vix", "vix"), "WTI": ("oil-wti", "petrol-wti"),
              "GOLD": ("gold", "aur"), "SILVER": ("silver", "argint"), "EURUSD": ("eurusd", "eurusd"),
              "GBPUSD": ("gbpusd", "gbpusd"), "USDJPY": ("usdjpy", "usdjpy"), "NVIDIA": ("nvidia", "nvidia"),
              "GOOGLE": ("google", "google"), "MICROSOFT": ("microsoft", "microsoft"), "C3AI": ("c3ai", "c3ai")}


def sb(path: str):
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/{path}", headers={"apikey": ANON, "Authorization": f"Bearer {ANON}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def long_date(d: str, lang: str) -> str:
    x = date.fromisoformat(d)
    if lang == "en":
        return f"{DAY_EN[x.weekday()]}, {MON_EN[x.month - 1]} {x.day}, {x.year}"
    return f"{DAY_RO[x.weekday()]}, {x.day} {MON_RO[x.month - 1]} {x.year}"


def short_date(d: str, lang: str) -> str:
    x = date.fromisoformat(d)
    return f"{MON_EN[x.month - 1][:3]} {x.day}, {x.year}" if lang == "en" else f"{x.day} {MON_RO[x.month - 1]} {x.year}"


def text_of(fragment: str) -> str:
    t = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def clip(s: str, n: int = 155) -> str:
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


# ------------------------------------------------------------------------------------------------
# Sablon de pagina
# ------------------------------------------------------------------------------------------------

CSS = """
:root{--bg:#EEF1F5;--ink:#13223A;--muted:#5A6B82;--line:#D5DCE6;--gold:#D9A441;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Archivo',-apple-system,Segoe UI,Arial,sans-serif;font-size:16px;line-height:1.6}
header{background:#13223A}
.hb{max-width:820px;margin:0 auto;padding:12px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:800;font-size:21px;font-stretch:125%}
.hb nav{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap}
.hb nav a{color:#C9D5E6;text-decoration:none;font-weight:600;font-size:14px;padding:6px 10px;border-radius:8px}
.hb nav a:hover{color:#fff;background:rgba(255,255,255,.08)}
.hb nav a.lang{border:1px solid rgba(255,255,255,.28);border-radius:999px;font-size:12.5px}
main{max-width:820px;margin:0 auto;padding:24px 16px 40px}
h1{font-size:clamp(26px,4.6vw,38px);line-height:1.12;font-stretch:75%;margin:0 0 6px}
.lede{color:var(--muted);margin:0 0 16px;max-width:70ch}
.cta{display:inline-block;background:var(--gold);color:#13223A;font-weight:700;text-decoration:none;border-radius:999px;padding:8px 16px;margin:4px 0 18px}
.report{background:#f3f4f6;border-radius:14px;overflow:hidden;font-size:14px;line-height:1.5;color:#111827}
.report body,.report *{font-family:'Archivo',-apple-system,Segoe UI,Arial,sans-serif}
.pager{display:flex;justify-content:space-between;gap:12px;margin:22px 0 0;font-size:14px;flex-wrap:wrap}
.pager a{color:var(--ink);font-weight:600}
.arch{list-style:none;padding:0;margin:0}
.arch li{padding:10px 0;border-bottom:1px solid var(--line)}
.arch a{color:var(--ink);font-weight:700;text-decoration:none}
.arch a:hover{text-decoration:underline}
.arch .m{color:var(--muted);font-size:13.5px}
h2.sec{font-size:19px;margin:28px 0 8px}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:13px}
footer div{max-width:820px;margin:0 auto;padding:18px 16px 32px}
footer a{color:inherit}
@media (max-width:560px){.hb nav{margin-left:0;width:100%}}
"""

LOGO = ('<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#D9A441"/>'
        '<rect x="7" y="13" width="4" height="12" rx="1" fill="#13223A"/><rect x="14" y="7" width="4" height="18" rx="1" fill="#13223A"/>'
        '<rect x="21" y="16" width="4" height="9" rx="1" fill="#13223A"/></svg>')

UI = {
    "en": {"today": "Today's report", "archive": "Archive", "about": "About us", "about_url": "/about.html",
           "home": "/?lang=en", "other": "Română", "terms": ("Terms &amp; conditions", "/terms.html"),
           "privacy": ("Privacy", "/privacy.html"), "disc": "For information only, not investment advice",
           "cta": "Open the interactive report", "archive_url": "/en/", "prev": "Previous report", "next": "Next report",
           "charts": "Interactive hourly charts are available in the live report on dailymarketlab.com."},
    "ro": {"today": "Raportul zilei", "archive": "Arhivă", "about": "Despre noi", "about_url": "/despre.html",
           "home": "/?lang=ro", "other": "English", "terms": ("Termeni și condiții", "/termeni.html"),
           "privacy": ("Confidențialitate", "/confidentialitate.html"), "disc": "Informativ, nu este consultanță de investiții",
           "cta": "Deschide raportul interactiv", "archive_url": "/ro/", "prev": "Raportul anterior", "next": "Raportul următor",
           "charts": "Graficele orare interactive sunt în raportul de pe dailymarketlab.com."},
}


def page(lang: str, path: str, title: str, desc: str, body: str, alt: dict[str, str] | None = None,
         other_url: str | None = None, ld: dict | None = None) -> str:
    u = UI[lang]
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{p}">\n' for l, p in (alt or {}).items())
    ldj = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n' if ld else ""
    other = other_url or ("/ro/" if lang == "en" else "/en/")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
{alts}<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<style>{CSS}</style>
{ldj}<script src="/ga.js" defer></script>
</head>
<body>
<header><div class="hb"><a class="logo" href="{u['home']}">{LOGO}Daily Market</a>
<nav><a href="{u['home']}">{u['today']}</a><a href="{u['archive_url']}">{u['archive']}</a><a href="{u['about_url']}">{u['about']}</a>
<a class="lang" href="{other}" hreflang="{'ro' if lang == 'en' else 'en'}">{u['other']}</a></nav></div></header>
<main>
{body}
</main>
<script>try{{if(localStorage.getItem("dm_nostat")!=="1")fetch("https://atlxahrvzhzrzfhmwwen.supabase.co/functions/v1/track",{{method:"POST",keepalive:true,headers:{{"Content-Type":"text/plain"}},body:JSON.stringify({{ev:"view",name:"page",path:location.pathname,lang:"{lang}",ref:document.referrer,tz:(Intl.DateTimeFormat().resolvedOptions().timeZone||"")}})}}).catch(function(){{}})}}catch(e){{}}</script>
<footer><div>© {date.today().year} Daily Market · {u['disc']} · <a href="{u['archive_url']}">{u['archive']}</a> ·
<a href="{u['about_url']}">{u['about']}</a> · <a href="{u['terms'][1]}">{u['terms'][0]}</a> · <a href="{u['privacy'][1]}">{u['privacy'][0]}</a></div></footer>
</body>
</html>
"""


def org_ld():
    return {"@type": "Organization", "name": "Daily Market", "url": SITE, "logo": f"{SITE}/favicon.svg"}


# ------------------------------------------------------------------------------------------------
# Rapoarte zilnice
# ------------------------------------------------------------------------------------------------

def report_path(d: str, lang: str) -> str:
    return f"/en/market-report-{d}.html" if lang == "en" else f"/ro/raport-piete-{d}.html"


def report_body(full_html: str) -> str:
    m = re.search(r"<body[^>]*>(.*)</body>", full_html, flags=re.S)
    b = m.group(1) if m else full_html
    # graficele cu lumanari (mari, interactive) raman doar in raportul live
    b = re.sub(r'<div class="dt-chart"><svg.*?</svg></div>', "", b, flags=re.S)
    b = re.sub(r'<div class="dt-hov">.*?</div>', "", b, flags=re.S)
    return b


def report_desc(full_html: str, lang: str, d: str) -> str:
    m = re.search(r'<div class="db-lead">(.*?)</div>', full_html, flags=re.S)
    lead = text_of(m.group(1)) if m else ""
    if not lead:
        lead = ("Daily market report: indices, commodities, currencies and stocks." if lang == "en" else
                "Raport zilnic: indici, mărfuri, valute și acțiuni.")
    return clip(lead)


def build_report(row: dict, lang: str, prev_d: str | None, next_d: str | None, has: dict) -> None:
    d = row["session_date"]
    src = row["html_en"] if lang == "en" else row["html"]
    u = UI[lang]
    title = (f"Market report for {long_date(d, 'en')}: SP500, DAX, gold, oil, EUR/USD, Nvidia | Daily Market" if lang == "en"
             else f"Raportul piețelor, {long_date(d, 'ro')}: SP500, DAX, aur, petrol, EUR/USD | Daily Market")
    h1 = (f"Markets on {long_date(d, 'en')}" if lang == "en" else f"Piețele zilei: {long_date(d, 'ro')}")
    desc = report_desc(src, lang, d)
    other_lang = "ro" if lang == "en" else "en"
    alt = {lang: report_path(d, lang)}
    if has.get((d, other_lang)):
        alt[other_lang] = report_path(d, other_lang)
    nav = ""
    if prev_d or next_d:
        nav = ('<div class="pager">'
               + (f'<a href="{report_path(prev_d, lang)}">← {u["prev"]}: {short_date(prev_d, lang)}</a>' if prev_d else "<span></span>")
               + (f'<a href="{report_path(next_d, lang)}">{u["next"]}: {short_date(next_d, lang)} →</a>' if next_d else "")
               + "</div>")
    body = (f'<h1>{html.escape(h1)}</h1><p class="lede">{html.escape(desc)}</p>'
            f'<a class="cta" href="{u["home"]}">{u["cta"]}</a>'
            f'<div class="report">{report_body(src)}</div>'
            f'<p class="lede" style="margin-top:12px;font-size:13px">{u["charts"]}</p>{nav}')
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc,
          "datePublished": d, "dateModified": d, "inLanguage": lang, "author": org_ld(), "publisher": org_ld(),
          "mainEntityOfPage": f"{SITE}{report_path(d, lang)}", "image": f"{SITE}/og.png"}
    out = ROOT / report_path(d, lang).lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(lang, report_path(d, lang), title, desc, body, alt,
                        alt.get(other_lang) or ("/ro/" if lang == "en" else "/en/"), ld), encoding="utf-8")


# ------------------------------------------------------------------------------------------------
# Weekly View: o pagina pe instrument
# ------------------------------------------------------------------------------------------------

def weekly_path(week: str, asset: str, lang: str) -> str:
    en, ro = ASSET_SLUG.get(asset, (asset.lower(), asset.lower()))
    return f"/en/weekly/{en}-outlook-{week}.html" if lang == "en" else f"/ro/weekly/{ro}-perspectiva-{week}.html"


def weekly_panels(full_html: str) -> list[dict]:
    out = []
    for chunk in full_html.split('<div class="wv-p" id="wvp-')[1:]:
        asset, rest = chunk.split('">', 1)
        i = rest.find('font-style:italic">')
        end = rest.find("</div></div>", i) + len("</div></div>") if i >= 0 else len(rest)
        panel = rest[:end]
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", panel, flags=re.S)
        watch = re.search(r'<div style="margin-top:12px">(.*?)</div>', panel, flags=re.S)
        out.append({"asset": asset, "html": panel, "title": text_of(h2.group(1)) if h2 else asset,
                    "desc": clip(text_of(watch.group(1))) if watch else ""})
    return out


def build_weekly(row: dict, lang: str, has_other: set) -> list[dict]:
    week = row["week_start"]
    src = row["html_en"] if lang == "en" else row["html"]
    items = []
    other_lang = "ro" if lang == "en" else "en"
    for p in weekly_panels(src):
        path = weekly_path(week, p["asset"], lang)
        title = f"{p['title']} | Weekly View · Daily Market"
        h_week = (f"Weekly View · week of {short_date(week, 'en')}" if lang == "en" else f"Weekly View · săptămâna din {short_date(week, 'ro')}")
        alt = {lang: path}
        if (week, p["asset"]) in has_other:
            alt[other_lang] = weekly_path(week, p["asset"], other_lang)
        body = (f'<p class="lede" style="margin:0 0 4px;font-weight:700">{html.escape(h_week)}</p>'
                f'<h1>{html.escape(p["title"])}</h1>'
                f'<a class="cta" href="{UI[lang]["home"]}">{UI[lang]["cta"]}</a>'
                f'<div class="report" style="padding:4px">{re.sub(r"<h2[^>]*>.*?</h2>", "", p["html"], count=1, flags=re.S)}</div>')
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"],
              "datePublished": week, "dateModified": week, "inLanguage": lang, "author": org_ld(), "publisher": org_ld(),
              "mainEntityOfPage": f"{SITE}{path}", "image": f"{SITE}/og.png"}
        out = ROOT / path.lstrip("/")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang, path, title, p["desc"] or title, body, alt,
                            alt.get(other_lang) or ("/ro/" if lang == "en" else "/en/"), ld), encoding="utf-8")
        items.append({"path": path, "title": p["title"], "week": week, "asset": p["asset"]})
    return items


# ------------------------------------------------------------------------------------------------
# Arhive, sitemap, linkuri pe pagina principala
# ------------------------------------------------------------------------------------------------

def build_archive(lang: str, reports: list[str], weeklies: list[dict]) -> None:
    u = UI[lang]
    path = u["archive_url"]
    title = ("Daily market reports archive: SP500, DAX, gold, oil, forex, stocks | Daily Market" if lang == "en"
             else "Arhiva rapoartelor zilnice: SP500, DAX, aur, petrol, valute, acțiuni | Daily Market")
    desc = ("Quantitative methods, tested on almost 20 years of market history. Every Daily Market report: options positioning, technical analysis, Fear & Greed sentiment, next-session "
            "forecast ranges and weekly outlooks for indices, commodities, currencies and stocks." if lang == "en" else
            "Metode cantitative, testate pe aproape 20 de ani de istoric. Toate rapoartele Daily Market: poziționarea din opțiuni, analiza tehnică, sentimentul Frică & Lăcomie, "
            "intervale pentru sesiunea următoare și perspective săptămânale.")
    h1 = "Market report archive" if lang == "en" else "Arhiva rapoartelor"
    wk = ""
    if weeklies:
        latest = max(w["week"] for w in weeklies)
        lst = "".join(f'<li><a href="{w["path"]}">{html.escape(w["title"])}</a></li>'
                      for w in weeklies if w["week"] == latest)
        older = sorted({w["week"] for w in weeklies if w["week"] != latest}, reverse=True)
        more = "".join(
            f'<li><span class="m">{short_date(x, lang)}:</span> ' + " · ".join(
                f'<a href="{w["path"]}" style="font-weight:600">{html.escape(w["asset"])}</a>' for w in weeklies if w["week"] == x)
            + "</li>" for x in older)
        wk = (f'<h2 class="sec">Weekly View · {"week of" if lang == "en" else "săptămâna din"} {short_date(latest, lang)}</h2>'
              f'<ul class="arch">{lst}{more}</ul>')
    rep = "".join(f'<li><a href="{report_path(d, lang)}">{html.escape(long_date(d, lang))}</a></li>' for d in reports)
    body = (f'<h1>{h1}</h1><p class="lede">{html.escape(desc)}</p>{wk}'
            f'<h2 class="sec">{"Daily reports" if lang == "en" else "Rapoarte zilnice"}</h2><ul class="arch">{rep}</ul>')
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": h1, "description": desc, "inLanguage": lang,
          "publisher": org_ld(), "url": f"{SITE}{path}"}
    (ROOT / path.strip("/")).mkdir(parents=True, exist_ok=True)
    (ROOT / path.strip("/") / "index.html").write_text(
        page(lang, path, title, desc, body, {"en": "/en/", "ro": "/ro/"}, "/ro/" if lang == "en" else "/en/", ld), encoding="utf-8")


def build_sitemap(urls: list[tuple[str, str, str, str]]) -> None:
    """urls: (path, lastmod, changefreq, priority)"""
    rows = "\n".join(f"  <url><loc>{SITE}{html.escape(p)}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "")
                     + f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>" for p, lm, cf, pr in urls)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n",
                                      encoding="utf-8")


def update_home_links(latest_en: str | None, latest_ro: str | None, weeklies_en: list[dict]) -> None:
    """Linkuri statice (vizibile pentru Google) in subsolul paginii principale."""
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    a, b = "<!--LATEST:start-->", "<!--LATEST:end-->"
    if a not in s:
        return
    parts = ['<a href="/en/">Report archive</a>', '<a href="/ro/" hreflang="ro">Arhiva rapoartelor</a>']
    if latest_en:
        parts.append(f'<a href="{report_path(latest_en, "en")}">Market report {short_date(latest_en, "en")}</a>')
    if latest_ro:
        parts.append(f'<a href="{report_path(latest_ro, "ro")}" hreflang="ro">Raportul din {short_date(latest_ro, "ro")}</a>')
    if weeklies_en:
        wk = max(w["week"] for w in weeklies_en)
        parts += [f'<a href="{w["path"]}">{html.escape(w["asset"])} weekly outlook</a>' for w in weeklies_en if w["week"] == wk][:4]
    block = a + '<div class="latest">' + " · ".join(parts) + "</div>" + b
    s = s[: s.index(a)] + block + s[s.index(b) + len(b):]
    p.write_text(s, encoding="utf-8")


def main() -> None:
    idx = sb("reports?select=session_date&order=session_date.desc&limit=2000")
    dates = [r["session_date"] for r in idx]
    if not dates:
        print("Niciun raport.")
        return
    # ce exista deja pe disc
    have = {(d, l) for d in dates for l in ("en", "ro") if (ROOT / report_path(d, l).lstrip("/")).exists()}
    need = [d for d in dates if (d, "ro") not in have or (d, "en") not in have] + dates[:REBUILD_LAST]
    need = sorted(set(need), reverse=True)
    rows = {}
    for i in range(0, len(need), 5):  # rapoartele sunt mari: cate 5 pe cerere
        batch = need[i:i + 5]
        for r in sb("reports?select=session_date,html,html_en&session_date=in.(" + ",".join(batch) + ")"):
            rows[r["session_date"]] = r
    # disponibilitatea limbilor (pentru hreflang): RO exista mereu; EN daca avem html_en sau pagina deja generata
    en_ok = {d for d in dates if (d, "en") in have}
    en_ok |= {d for d, r in rows.items() if r.get("html_en")}
    has = {(d, "ro"): True for d in dates}
    has.update({(d, "en"): True for d in en_ok})
    ro_dates, en_dates = dates, [d for d in dates if d in en_ok]
    for d, r in rows.items():
        for lang, lst in (("ro", ro_dates), ("en", en_dates)):
            if lang == "en" and not r.get("html_en"):
                continue
            i = lst.index(d)
            build_report(r, lang, lst[i + 1] if i + 1 < len(lst) else None, lst[i - 1] if i > 0 else None, has)
        print("raport", d, "en" if r.get("html_en") else "", "ro")

    # Weekly View (putine randuri: le refacem pe toate)
    weeks = sb("weekly_views?select=week_start,html,html_en&order=week_start.desc&limit=60")
    w_en, w_ro = [], []
    for w in weeks:
        en_assets = {(w["week_start"], p["asset"]) for p in weekly_panels(w["html_en"])} if w.get("html_en") else set()
        ro_assets = {(w["week_start"], p["asset"]) for p in weekly_panels(w["html"])}
        w_ro += build_weekly(w, "ro", en_assets)
        if w.get("html_en"):
            w_en += build_weekly(w, "en", ro_assets)
        print("weekly", w["week_start"], "en" if w.get("html_en") else "", "ro")

    build_archive("en", en_dates, w_en)
    build_archive("ro", ro_dates, w_ro)
    update_home_links(en_dates[0] if en_dates else None, ro_dates[0] if ro_dates else None, w_en)

    today = date.today().isoformat()
    urls = [("/", today, "daily", "1.0"), ("/en/", today, "daily", "0.9"), ("/ro/", today, "daily", "0.8"),
            ("/?lang=ro", today, "daily", "0.8"), ("/about.html", "", "monthly", "0.6"), ("/despre.html", "", "monthly", "0.5"),
            ("/terms.html", "", "yearly", "0.2"), ("/privacy.html", "", "yearly", "0.2"),
            ("/termeni.html", "", "yearly", "0.2"), ("/confidentialitate.html", "", "yearly", "0.2")]
    urls += [(report_path(d, "en"), d, "never", "0.7") for d in en_dates]
    urls += [(report_path(d, "ro"), d, "never", "0.6") for d in ro_dates]
    urls += [(w["path"], w["week"], "never", "0.7") for w in w_en]
    urls += [(w["path"], w["week"], "never", "0.6") for w in w_ro]
    build_sitemap(urls)
    print(f"Gata: {len(en_dates)} rapoarte EN, {len(ro_dates)} RO, {len(w_en)} + {len(w_ro)} pagini Weekly View, "
          f"{len(urls)} adrese in sitemap")


if __name__ == "__main__":
    sys.exit(main())
