#!/usr/bin/env python3
"""Meniul comun al site-ului (acelasi pe toate paginile, ca pe prima pagina):
Raport zilnic · Weekly View · Produse · Acuratețe · [Portofoliu] [Abonează-te] · RO/EN/DE.
- header(lang, alt) e folosit de generatoare (build_pages, tools_products, tools_accuracy);
- rulat direct, inlocuieste <header>…</header> in paginile statice (despre, termeni, confidentialitate etc.).
Paginile de reclama (pick.html, pick-en.html, pick-de.html) raman fara meniu, intentionat."""
from __future__ import annotations

import re
from pathlib import Path

LOGO = ('<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#D9A441"/>'
        '<rect x="7" y="13" width="4" height="12" rx="1" fill="#13223A"/><rect x="14" y="7" width="4" height="18" rx="1" fill="#13223A"/>'
        '<rect x="21" y="16" width="4" height="9" rx="1" fill="#13223A"/></svg>')

# paginile echivalente in cele trei limbi (pentru comutatorul de limba)
PAGES = {
    "products": {"ro": "/produse.html", "en": "/products.html", "de": "/produkte.html"},
    "accuracy": {"ro": "/acuratete.html", "en": "/accuracy.html", "de": "/genauigkeit.html"},
    "about": {"ro": "/despre.html", "en": "/about.html", "de": "/ueber-uns.html"},
    "terms": {"ro": "/termeni.html", "en": "/terms.html", "de": "/agb.html"},
    "privacy": {"ro": "/confidentialitate.html", "en": "/privacy.html", "de": "/datenschutz.html"},
    "unsub": {"ro": "/dezabonare.html", "en": "/unsubscribe.html", "de": "/abmelden.html"},
    "impressum": {"ro": "/impressum.html", "en": "/impressum.html", "de": "/impressum.html"},
}

T = {
    "ro": dict(daily="Raport zilnic", weekly="Weekly View", products="Produse", accuracy="Acuratețe", pf="Portofoliu", sub="Abonează-te"),
    "en": dict(daily="Daily Report", weekly="Weekly View", products="Products", accuracy="Accuracy", pf="Portfolio", sub="Subscribe"),
    "de": dict(daily="Bericht", weekly="Weekly View", products="Produkte", accuracy="Trefferquote", pf="Portfolio", sub="Abonnieren"),
}

CSS = """
header.dmh{background:#13223A;color:#fff}
.dmh .dmb{max-width:1080px;margin:0 auto;padding:12px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.dmh a{display:inline-flex;align-items:center;width:auto;max-width:none;margin:0;gap:0;font-stretch:100%;text-decoration:none;color:inherit;line-height:1.3}
.dmh .dml{gap:10px;color:#fff;font-weight:800;font-size:21px;font-stretch:125%;padding:0}
.dmh .dms{flex:1}
.dmh .dmn{display:flex;gap:2px}
.dmh .dmn a{color:#C9D5E6;font-weight:600;font-size:15px;padding:8px 12px;border-radius:8px}
.dmh .dmn a:hover{color:#fff;background:rgba(255,255,255,.08)}
.dmh .dmn a.on{color:#fff;box-shadow:inset 0 -2px 0 #D9A441;border-radius:0}
.dmh .dmp{color:#D9A441;border:1px solid #D9A441;font-weight:700;font-size:15px;border-radius:999px;padding:7px 15px}
.dmh .dmp:hover{background:rgba(217,164,65,.14)}
.dmh .dmu{background:#D9A441;color:#13223A;font-weight:700;font-size:15px;border-radius:999px;padding:8px 16px}
.dmh .dmg{display:flex;gap:4px}
.dmh .dmg a{color:#C9D5E6;border:1px solid rgba(255,255,255,.28);font-weight:700;font-size:12.5px;border-radius:999px;padding:6px 9px;letter-spacing:.4px}
.dmh .dmg a.on{color:#13223A;background:#C9D5E6;border-color:#C9D5E6}
@media (max-width:760px){
 .dmh .dmb{padding:10px 14px;gap:8px}
 .dmh .dml{font-size:19px}
 .dmh .dmp,.dmh .dmu{padding:6px 11px;font-size:13px}
 .dmh .dmn{order:5;flex:1 0 100%;margin:2px -4px 0}
 .dmh .dmn a{flex:1 1 auto;justify-content:center;padding:9px 5px;font-size:13.5px;white-space:nowrap}
 .dmh .dmg{order:4}
 .dmh .dmg a{padding:5px 7px;font-size:11.5px}
}
"""


def header(lang: str, alt: dict[str, str] | None = None, active: str = "") -> str:
    """alt = {lang: url} pentru comutatorul de limba (lipsa = prima pagina in limba respectiva)."""
    t = T[lang]
    home = f"/?lang={lang}"
    p = PAGES
    nav = [("daily", home), ("weekly", home + "#weekly"), ("products", p["products"][lang]), ("accuracy", p["accuracy"][lang])]
    on = ' class="on"'
    links = "".join(f'<a href="{u}"{on if k == active else ""}>{t[k]}</a>' for k, u in nav)
    alt = alt or {}
    langs = "".join(f'<a href="{alt.get(lg) or "/?lang=" + lg}" hreflang="{lg}"{on if lg == lang else ""}>{lg.upper()}</a>'
                    for lg in ("ro", "en", "de"))
    return (f'<style>{CSS}</style><header class="dmh"><div class="dmb">'
            f'<a class="dml" href="{home}">{LOGO}Daily Market</a><div class="dms"></div>'
            f'<nav class="dmn">{links}</nav>'
            f'<a class="dmp" href="{home}#portofoliu">{t["pf"]}</a>'
            f'<a class="dmu" href="{home}&amp;sub=1">{t["sub"]}</a>'
            f'<div class="dmg">{langs}</div></div></header>')


def apply_static(root: Path) -> list[str]:
    done = []
    for key, by in PAGES.items():
        for lang, url in by.items():
            f = root / url.lstrip("/")
            if not f.exists() or (key == "impressum" and lang != "de"):
                continue
            s = f.read_text(encoding="utf-8")
            new = header(lang, by if key != "impressum" else None, active="products" if key == "products" else
                         "accuracy" if key == "accuracy" else "")
            s2, n = re.subn(r"(?:<style>\s*header\.dmh.*?</style>)?<header\b.*?</header>", lambda m: new, s, count=1, flags=re.S)
            if n:
                f.write_text(s2, encoding="utf-8")
                done.append(url)
    return done


if __name__ == "__main__":
    print("\n".join(apply_static(Path(__file__).resolve().parent)))
