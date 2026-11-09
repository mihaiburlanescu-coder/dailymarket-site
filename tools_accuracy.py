#!/usr/bin/env python3
"""Genereaza paginile „Acuratețe” (acuratete.html) si „Accuracy” (accuracy.html).
Cifrele vin live din Supabase (functia publica dm_accuracy), deci pagina se actualizeaza singura. Ruleaza: python3 tools_accuracy.py"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = re.search(r'const SUPABASE_ANON = "([^"]+)"', (HERE / "index.html").read_text(encoding="utf-8")).group(1)
URL = "https://atlxahrvzhzrzfhmwwen.supabase.co"
LOGO = ('<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#D9A441"/>'
        '<rect x="7" y="13" width="4" height="12" rx="1" fill="#13223A"/><rect x="14" y="7" width="4" height="18" rx="1" fill="#13223A"/>'
        '<rect x="21" y="16" width="4" height="9" rx="1" fill="#13223A"/></svg>')

T = {
 "ro": dict(
  file="acuratete.html", alt="accuracy.html", home="./?lang=ro", locale="ro-RO",
  title="Acuratețe · Daily Market", desc="Cât de bine au ieșit predicțiile Daily Market: rezultate live, actualizate zilnic, inclusiv greșelile.",
  h1="Cât de bine <span>nimerim?</span>",
  lead="Publicăm toate rezultatele, inclusiv pe cele care nu ies. Cifrele de mai jos se actualizează automat în fiecare zi, din aceleași date pe care le folosește raportul.",
  loading="Se încarcă rezultatele…", err="Rezultatele nu au putut fi încărcate acum. Reîncearcă peste câteva minute.",
  upd="Actualizat", live="Live", hist="Testat pe istoric", promise="Ce promitem",
  r_t="Intervalele de preț", r_tag="Predicție · ziua următoare",
  r_p="Prețul de închidere al zilei următoare cade în intervalul de 70% în aproximativ 7 cazuri din 10 și în intervalul de 90% în aproximativ 9 din 10.",
  r_l="{in70} din {n} închideri în intervalul de 70% ({p70}) · {in90} din {n} în intervalul de 90% ({p90}) · din {from}",
  r_h="Intervalele sunt calculate din prețul opțiunilor și calibrate pe 2008–2026 să nimerească aceste procente.",
  r_c="Cum evoluează rezultatul live (cumulat)", b70="în intervalul de 70% (ținta: ~70%)", b90="în intervalul de 90% (ținta: ~90%)", t70="ținta 70%", t90="ținta 90%",
  p_t="Pick of the Day", p_tag="5 zile",
  p_p="O singură idee pe zi, cu țintă și stop. Avantajul e mic, dar real: mai multe pick-uri pe plus decât la întâmplare.",
  p_h="Testat pe 2008–2026: 53% din pick-uri pe plus după 5 zile, față de 50% la întâmplare – la fel în ambele jumătăți ale perioadei.",
  p_l="{n} pick-uri încheiate, {win} pe plus, rezultat mediu {avg} · din {from}",
  p_few="Încă prea puține ca să conteze statistic: procentul are sens după cel puțin 20 de pick-uri.",
  p_none="Primele pick-uri sunt încă deschise.",
  f_t="Portofoliul lunar", f_tag="o lună",
  f_p="Strategie pe trend, reconstruită lunar, cu risc egal pe poziții și stop pe fiecare poziție. Scopul: câștiguri constante cu scăderi mici.",
  f_h="Testat pe 2008–2026: în medie +6,7% pe an, cea mai mare scădere de la un vârf −21%.",
  f_l="{value} față de 10.000 la start ({ret}) · {closed} poziții încheiate, {win} pe plus, în total {pnl} · din {from}",
  f_c="Valoarea portofoliului virtual",
  n_t="Ce nu prezicem", n_tag="spus deschis",
  n_p="Verdictele BUY/SELL din raport descriu trendul de acum. Nu sunt o predicție a direcției de mâine – pe termen foarte scurt, direcția e aproape o aruncare cu banul, pentru oricine.",
  n_l="Live, verdictul a arătat direcția zilei următoare în {ok} din {n} cazuri ({p}).",
  n_h="Pe 2007–2026, semnalul tehnic singur nu a prezis direcția zilelor următoare mai bine decât întâmplarea. De aceea nu îl vindem ca predicție.",
  why="De ce publicăm și greșelile", why_p="Oricine poate afișa câștigurile. Un instrument în care poți avea încredere îți arată și cât de des greșește – și te lasă să verifici singur.",
  disc="Informativ și educativ, nu este consultanță de investiții. Rezultatele trecute nu garantează rezultate viitoare. Tranzacționarea implică un risc ridicat de pierdere a capitalului.",
  foot='<a href="./?lang=ro">Înapoi la raport</a> · <a href="produse.html">Produsele noastre</a> · <a href="despre.html">Despre noi</a> · <a href="termeni.html">Termeni și condiții</a> · <a href="confidentialitate.html">Confidențialitate</a> · <a href="accuracy.html" lang="en" hreflang="en">English</a>',
  cta="Primește Pick of the Day pe email", cta_url="./?lang=ro&sub=1"),
 "en": dict(
  file="accuracy.html", alt="acuratete.html", home="./", locale="en-GB",
  title="Accuracy · Daily Market", desc="How well Daily Market forecasts did: live results, updated daily, mistakes included.",
  h1="How often are we <span>right?</span>",
  lead="We publish every result, including the ones that don't work out. The figures below update automatically every day, from the same data the report uses.",
  loading="Loading results…", err="The results could not be loaded right now. Please try again in a few minutes.",
  upd="Updated", live="Live", hist="Tested on history", promise="What we promise",
  r_t="Price ranges", r_tag="Forecast · next session",
  r_p="The next session's close lands inside the 70% range about 7 times out of 10, and inside the 90% range about 9 times out of 10.",
  r_l="{in70} of {n} closes inside the 70% range ({p70}) · {in90} of {n} inside the 90% range ({p90}) · since {from}",
  r_h="The ranges are computed from option prices and calibrated on 2008–2026 to hit these percentages.",
  r_c="How the live result evolves (cumulative)", b70="inside the 70% range (aim: ~70%)", b90="inside the 90% range (aim: ~90%)", t70="70% target", t90="90% target",
  p_t="Pick of the Day", p_tag="5 days",
  p_p="One idea a day, with a target and a stop. The edge is small but real: more picks end positive than at random.",
  p_h="Tested on 2008–2026: 53% of picks positive after 5 days, versus 50% at random – the same in both halves of the period.",
  p_l="{n} closed picks, {win} positive, average result {avg} · since {from}",
  p_few="Still too few to mean anything statistically: the percentage makes sense after at least 20 picks.",
  p_none="The first picks are still open.",
  f_t="Monthly portfolio", f_tag="one month",
  f_p="A trend strategy rebuilt monthly, with equal risk per position and a stop on every position. The aim: steady gains with small drawdowns.",
  f_h="Tested on 2008–2026: +6.7% a year on average, largest fall from a peak −21%.",
  f_l="{value} versus 10,000 at the start ({ret}) · {closed} closed positions, {win} positive, {pnl} in total · since {from}",
  f_c="Value of the virtual portfolio",
  n_t="What we don't predict", n_tag="said openly",
  n_p="The BUY/SELL verdicts in the report describe the current trend. They are not a forecast of tomorrow's direction – over very short horizons, direction is close to a coin flip, for anyone.",
  n_l="Live, the verdict matched the next session's direction in {ok} of {n} cases ({p}).",
  n_h="On 2007–2026, the technical signal alone did not predict the next days' direction better than chance. That is why we don't sell it as a forecast.",
  why="Why we publish our mistakes too", why_p="Anyone can show their wins. A tool you can trust also shows how often it is wrong – and lets you check for yourself.",
  disc="For information and education only, not investment advice. Past results do not guarantee future results. Trading carries a high risk of losing capital.",
  foot='<a href="./">Back to the report</a> · <a href="products.html">Our products</a> · <a href="about.html">About us</a> · <a href="terms.html">Terms &amp; conditions</a> · <a href="privacy.html">Privacy</a> · <a href="acuratete.html" lang="ro" hreflang="ro">Română</a>',
  cta="Get the Pick of the Day by email", cta_url="./?sub=1"),
}

CSS = """
:root{--bg:#EEF1F5;--card:#fff;--ink:#13223A;--muted:#5A6B82;--line:#D5DCE6;--soft:#f6f7fb;--up:#1A7F4B;--down:#C2362F;--gold:#D9A441;--grid:#e5e9f0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0C1420;--card:#131F31;--ink:#E7EDF5;--muted:#93A3B8;--line:#24344C;--soft:#1a2940;--up:#4CC38A;--down:#F0776E;--grid:#24344C}}
:root[data-theme="dark"]{--bg:#0C1420;--card:#131F31;--ink:#E7EDF5;--muted:#93A3B8;--line:#24344C;--soft:#1a2940;--up:#4CC38A;--down:#F0776E;--grid:#24344C}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Archivo',-apple-system,Segoe UI,Arial,sans-serif;font-size:16px;line-height:1.6}
header{background:#13223A}
header a{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:800;font-size:21px;font-stretch:125%;max-width:980px;margin:0 auto;padding:12px 16px}
.top{background:radial-gradient(120% 90% at 85% 0%,#2a4670 0%,#13223A 55%,#0b1524 100%);color:#fff}
.top .in{max-width:980px;margin:0 auto;padding:40px 16px 44px}
.top h1{font-size:clamp(32px,5.5vw,50px);line-height:1.05;margin:0;font-stretch:80%;letter-spacing:-.5px}
.top h1 span{color:#E7BE6A}
.top p{color:#C9D5E6;font-size:17px;max-width:62ch;margin:14px 0 0}
.top .upd{color:#93A3B8;font-size:13px;margin-top:12px}
main{max-width:980px;margin:0 auto;padding:26px 16px 40px;display:grid;gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 24px}
.card .hd{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.card h2{margin:0;font-size:22px}
.tag{font-size:12px;font-weight:700;letter-spacing:.4px;padding:3px 10px;border-radius:99px;background:var(--soft);color:var(--muted)}
.row{display:grid;grid-template-columns:160px 1fr;gap:6px 16px;margin-top:12px;align-items:baseline}
.row .k{font-size:12.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}
.row .v{font-size:15.5px}
.big{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0 4px}
.big div{background:var(--soft);border-radius:12px;padding:12px 16px;min-width:150px}
.big b{display:block;font-size:30px;line-height:1.1;font-weight:800}
.big span{font-size:13px;color:var(--muted)}
.note{font-size:14px;color:var(--muted);margin-top:8px}
.chart{margin-top:14px}
.chart .ct{font-size:13px;font-weight:700;color:var(--muted);margin-bottom:4px}
svg.ch{width:100%;height:auto;display:block}
.why{background:linear-gradient(135deg,#13223A,#2a4670);color:#fff;border:none}
.why p{color:#C9D5E6;margin:6px 0 0}
.cta a{display:inline-block;margin-top:14px;background:#D9A441;color:#13223A;font-weight:800;text-decoration:none;padding:10px 18px;border-radius:999px}
.disc{color:var(--muted);font-size:13px}
.err{color:var(--down)}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:13px}
footer div{max-width:980px;margin:0 auto;padding:18px 16px 32px}
footer a{color:inherit}
@media (max-width:640px){.row{grid-template-columns:1fr;gap:2px}.row .v{margin-bottom:8px}.card{padding:18px 16px}.big div{flex:1 1 40%;min-width:0}.big b{font-size:26px}}
"""

JS = r"""
const T = __T__;
const nf = (v, d = 0) => Number(v).toLocaleString(T.locale, { minimumFractionDigits: d, maximumFractionDigits: d });
const pct = (a, b) => b ? nf(100 * a / b, 0) + "%" : "–";
const dt = s => new Date(s + "T12:00:00").toLocaleDateString(T.locale, { day: "numeric", month: "long", year: "numeric" });
const fill = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k] ?? "");
const $ = id => document.getElementById(id);
function line(series, key, w, h, y0, y1, col, dash) {
  const n = series.length; if (n < 2) return "";
  const X = i => 62 + (w - 72) * i / (n - 1), Y = v => 10 + (h - 30) * (1 - (v - y0) / (y1 - y0));
  return `<polyline fill="none" stroke="${col}" stroke-width="3" stroke-linejoin="round" ${dash ? 'stroke-dasharray="6 5"' : ""} points="${series.map((p, i) => X(i).toFixed(1) + "," + Y(p[key]).toFixed(1)).join(" ")}"/>`;
}
function chart(series, keys, y0, y1, ticks, refs, box) {
  const w = Math.round(Math.min(900, Math.max(300, (box && box.clientWidth) || 900))), h = w < 600 ? 200 : 240, Y = v => 10 + (h - 30) * (1 - (v - y0) / (y1 - y0));
  let g = ticks.map(t => `<line x1="62" x2="${w - 10}" y1="${Y(t)}" y2="${Y(t)}" stroke="var(--grid)"/><text x="56" y="${Y(t) + 4}" text-anchor="end" font-size="12" fill="var(--muted)">${nf(t)}</text>`).join("");
  g += (refs || []).map(r => `<line x1="62" x2="${w - 10}" y1="${Y(r.v)}" y2="${Y(r.v)}" stroke="${r.c}" stroke-dasharray="4 4" opacity=".7"/><text x="${w - 12}" y="${Y(r.v) - 6}" text-anchor="end" font-size="12" fill="${r.c}">${r.t}</text>`).join("");
  g += keys.map(k => line(series, k.k, w, h, y0, y1, k.c)).join("");
  const a = series[0], b = series[series.length - 1];
  g += `<text x="62" y="${h - 4}" font-size="12" fill="var(--muted)">${dt(a.d)}</text><text x="${w - 10}" y="${h - 4}" text-anchor="end" font-size="12" fill="var(--muted)">${dt(b.d)}</text>`;
  return `<svg class="ch" viewBox="0 0 ${w} ${h}" role="img">${g}</svg>`;
}
(async () => {
  let A;
  try {
    const r = await fetch(__URL__ + "/rest/v1/rpc/dm_accuracy", { method: "POST",
      headers: { "Content-Type": "application/json", apikey: __KEY__, Authorization: "Bearer " + __KEY__ }, body: "{}" });
    if (!r.ok) throw new Error(r.status);
    A = await r.json();
  } catch (e) { $("upd").innerHTML = `<span class="err">${T.err}</span>`; return; }
  $("upd").textContent = T.upd + ": " + new Date(A.updated).toLocaleString(T.locale, { day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" });
  const R = A.ranges;
  if (R && R.n) {
    $("rBig").innerHTML = `<div><b style="color:${R.in70 / R.n >= .65 ? "var(--up)" : "var(--gold)"}">${pct(R.in70, R.n)}</b><span>${T.b70}</span></div>`
      + `<div><b style="color:${R.in90 / R.n >= .85 ? "var(--up)" : "var(--gold)"}">${pct(R.in90, R.n)}</b><span>${T.b90}</span></div>`;
    $("rLive").textContent = fill(T.r_l, { in70: R.in70, in90: R.in90, n: R.n, p70: pct(R.in70, R.n), p90: pct(R.in90, R.n), from: dt(R.from) });
    if (A.ranges_series.length > 1) $("rChart").innerHTML = `<div class="ct">${T.r_c}</div>` + chart(A.ranges_series,
      [{ k: "p70", c: "#2f6fd6" }, { k: "p90", c: "#7c4ddc" }], 40, 100, [40, 60, 80, 100],
      [{ v: 70, c: "#2f6fd6", t: T.t70 }, { v: 90, c: "#7c4ddc", t: T.t90 }], $("rChart"));
  }
  const P = A.pick;
  if (P && P.n) {
    $("pLive").textContent = fill(T.p_l, { n: P.n, win: P.win, avg: (P.avg_pct > 0 ? "+" : "") + nf(P.avg_pct, 2) + "%", from: dt(P.from) });
    if (P.n < 20) $("pFew").textContent = T.p_few;
  } else $("pLive").textContent = T.p_none;
  const F = A.portfolio;
  if (F && F.value) {
    const ret = (F.value / F.start - 1) * 100;
    $("fBig").innerHTML = `<div><b style="color:${ret >= 0 ? "var(--up)" : "var(--down)"}">${ret >= 0 ? "+" : ""}${nf(ret, 1)}%</b><span>${dt(F.from)} → ${dt(F.day)}</span></div>`;
    $("fLive").textContent = fill(T.f_l, { value: nf(F.value, 0), ret: (ret >= 0 ? "+" : "") + nf(ret, 1) + "%", closed: F.closed,
      win: F.closed_win, pnl: (F.closed_pnl >= 0 ? "+" : "") + nf(F.closed_pnl, 0), from: dt(F.from) });
    const s = F.series; if (s.length > 1) {
      const vs = s.map(x => x.v), lo = Math.floor(Math.min(...vs, F.start) / 100) * 100 - 100, hi = Math.ceil(Math.max(...vs, F.start) / 100) * 100 + 100;
      const st = Math.max(100, Math.round((hi - lo) / 4 / 100) * 100), tk = []; for (let t = lo; t <= hi; t += st) tk.push(t);
      $("fChart").innerHTML = `<div class="ct">${T.f_c}</div>` + chart(s, [{ k: "v", c: "#B7791F" }], lo, hi, tk, [{ v: F.start, c: "#5A6B82", t: nf(F.start) }], $("fChart"));
    }
  }
  const N = A.lean;
  if (N && N.n) $("nLive").textContent = fill(T.n_l, { ok: N.ok, n: N.n, p: pct(N.ok, N.n) });
})();
"""


def page(lg: str) -> str:
    t = T[lg]
    import json
    js = (JS.replace("__T__", json.dumps({k: t[k] for k in ("locale", "err", "upd", "t70", "r_l", "r_c", "p_l", "p_few", "p_none", "f_l", "f_c", "n_l", "t90", "b70", "b90")},
                                          ensure_ascii=False))
            .replace("__URL__", json.dumps(URL)).replace("__KEY__", json.dumps(KEY)))
    other = "en" if lg == "ro" else "ro"

    def card(title, tag, promise, live_id, hist, extra=""):
        return f"""<section class="card"><div class="hd"><h2>{title}</h2><span class="tag">{tag}</span></div>{extra}
<div class="row"><div class="k">{t["promise"]}</div><div class="v">{promise}</div>
<div class="k">{t["live"]}</div><div class="v" id="{live_id}">{t["loading"]}</div>
<div class="k">{t["hist"]}</div><div class="v">{hist}</div></div>"""

    return f"""<!doctype html>
<html lang="{lg}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t["title"]}</title><meta name="description" content="{t["desc"]}">
<link rel="canonical" href="https://dailymarketlab.com/{t["file"]}">
<link rel="alternate" hreflang="{lg}" href="https://dailymarketlab.com/{t["file"]}">
<link rel="alternate" hreflang="{other}" href="https://dailymarketlab.com/{t["alt"]}">
<meta property="og:title" content="{t["title"]}"><meta property="og:description" content="{t["desc"]}"><meta property="og:image" content="https://dailymarketlab.com/og.png">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<style>{CSS}</style><script src="/ga.js" defer></script></head><body>
<header><a href="{t["home"]}">{LOGO}Daily Market</a></header>
<div class="top"><div class="in"><h1>{t["h1"]}</h1><p>{t["lead"]}</p><div class="upd" id="upd">{t["loading"]}</div></div></div>
<main>
{card(t["r_t"], t["r_tag"], t["r_p"], "rLive", t["r_h"], '<div class="big" id="rBig"></div>')}<div class="chart" id="rChart"></div></section>
{card(t["p_t"], t["p_tag"], t["p_p"], "pLive", t["p_h"])}<div class="note" id="pFew"></div></section>
{card(t["f_t"], t["f_tag"], t["f_p"], "fLive", t["f_h"], '<div class="big" id="fBig"></div>')}<div class="chart" id="fChart"></div></section>
{card(t["n_t"], t["n_tag"], t["n_p"], "nLive", t["n_h"])}</section>
<section class="card why"><h2>{t["why"]}</h2><p>{t["why_p"]}</p><div class="cta"><a href="{t["cta_url"]}">{t["cta"]}</a></div></section>
<p class="disc">{t["disc"]}</p>
</main>
<footer><div>{t["foot"]}</div></footer>
<script>{js}</script>
</body></html>
"""


if __name__ == "__main__":
    for lg in ("ro", "en"):
        (HERE / T[lg]["file"]).write_text(page(lg), encoding="utf-8")
        print("scris", T[lg]["file"])
