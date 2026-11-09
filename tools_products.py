#!/usr/bin/env python3
"""Genereaza paginile „Produsele noastre” (produse.html) si „Our products” (products.html). Ruleaza: python3 tools_products.py"""
from pathlib import Path

LOGO = ('<svg width="{s}" height="{s}" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#D9A441"/>'
        '<rect x="7" y="13" width="4" height="12" rx="1" fill="#13223A"/><rect x="14" y="7" width="4" height="18" rx="1" fill="#13223A"/>'
        '<rect x="21" y="16" width="4" height="9" rx="1" fill="#13223A"/></svg>')
EMBLEM = {
    "athena": '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="26" fill="none" stroke="#6d4fe0" stroke-width="3"/><circle cx="32" cy="32" r="15" fill="none" stroke="#a48cf5" stroke-width="3"/><circle cx="32" cy="32" r="5" fill="#5b3fc4"/><path d="M32 4v10M32 50v10M4 32h10M50 32h10" stroke="#6d4fe0" stroke-width="3" stroke-linecap="round"/></svg>',
    "odyssey": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M14 40h36l-6 10H20z" fill="#0b6e80"/><path d="M32 10v28" stroke="#053b4a" stroke-width="3"/><path d="M33 12l14 22H33z" fill="#1fb3b0"/><path d="M31 16L19 34h12z" fill="#7fdcd6"/><path d="M8 54c6 0 6-3 12-3s6 3 12 3 6-3 12-3 6 3 12 3" fill="none" stroke="#0e9aa0" stroke-width="3" stroke-linecap="round"/></svg>',
    "portfolio": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 50l14-14 10 8 22-24" fill="none" stroke="#13223A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M44 20h10v10" fill="none" stroke="#D9A441" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="36" r="3.5" fill="#D9A441"/><circle cx="32" cy="44" r="3.5" fill="#D9A441"/></svg>',
}

T = {
"ro": {
 "file": "produse.html", "alt": "products.html", "lang": "ro", "home": "./?lang=ro",
 "title": "Produsele noastre · Daily Market", "h1": "Produsele <span>noastre</span>",
 "desc": "Athena, Odyssey și Portofoliul Daily Market: instrumente care transformă complexitatea piețelor în decizii clare și disciplinate.",
 "lead": "Instrumente construite pentru a transforma complexitatea piețelor financiare în decizii clare, disciplinate și bazate pe date.",
 "cta_contact": "Cere detalii", "cta_pf": "Vezi portofoliul live", "pf_url": "./?lang=ro#portofoliu",
 "mail_subj": "Detalii%20despre%20",
 "products": [
  ("athena", "Market Intelligence", "ATHENA", "Market Intelligence. Smarter Trading Decisions.",
   ["Athena este o platformă inteligentă de analiză a piețelor financiare, concepută pentru a transforma informațiile complexe din piața de opțiuni în semnale clare, relevante și ușor de interpretat.",
    "Într-un mediu financiar în care viteza, volatilitatea și volumul informațiilor fac diferența, Athena oferă o perspectivă suplimentară asupra oportunităților de tranzacționare, ajutând utilizatorii să ia decizii mai bine fundamentate."],
   [("Dincolo de analiza tradițională", "Spre deosebire de instrumentele convenționale care se concentrează pe evoluția istorică a prețurilor, Athena valorifică informații din piața de opțiuni, combinând analiza cantitativă cu inteligență artificială și învățare automată."),
    ("Inteligență transformată în acțiune", "Athena urmărește multiple instrumente financiare – acțiuni, indici, mărfuri și alte clase de active – oferind o perspectivă structurată și consecventă asupra piețelor monitorizate."),
    ("SIGNALS", "Fiecare semnal este însoțit de indicatori de încredere, pentru a fi evaluat în contextul propriului profil de risc."),
    ("Construită pentru piețe în continuă schimbare", "Adaptabilitate, evaluare continuă și disciplină statistică, fără dependență de interpretări subiective sau reacții emoționale. Arhitectura modulară permite extinderea instrumentelor monitorizate și integrarea în fluxuri de lucru automatizate.")],
   ("The Athena Advantage", "Mai puțin zgomot. Mai multă claritate. Decizii bazate pe date.",
    "Athena nu promite să prezică viitorul piețelor financiare. Misiunea sa este să transforme complexitatea lor într-un avantaj informațional – un instrument suplimentar pentru identificarea, evaluarea și prioritizarea oportunităților.",
    "Athena — Turning Market Complexity into Actionable Intelligence.")),
  ("odyssey", "DAX Automated Trading", "ODYSSEY", "Disciplină. Precizie. Consecvență.",
   ["Odyssey este un robot de tranzacționare complet automat, dedicat unei singure piețe: indicele german <b>DAX 40</b>. Nu se împrăștie pe zeci de instrumente și nu urmărește modele de moment. Face un singur lucru – și îl face cu disciplină, în fiecare zi de tranzacționare."],
   [("O singură piață, înțeleasă în profunzime", "DAX este unul dintre cei mai dinamici indici din Europa: mișcări rapide, volatilitate ridicată, oportunități zilnice. Odyssey a fost construit exclusiv pentru această piață și calibrat pe ritmul ei. Specializarea este avantajul lui."),
    ("Tranzacționare fără emoții", "Frica, lăcomia, graba sau dorința de a recupera o pierdere sunt cele mai mari capcane ale unui trader. Odyssey nu le are. Execută fiecare decizie după reguli clare și consecvente, de la prima tranzacție a zilei până la ultima."),
    ("Protecția capitalului, înainte de toate", "Fiecare poziție are riscul definit din momentul intrării. Mărimea poziției se calculează automat, profitul obținut este protejat pe parcurs, iar pierderile sunt limitate."),
    ("Mereu atent, niciodată obosit", "Odyssey urmărește piața fără pauză pe toată durata sesiunii și reacționează în timp real, fără întârzieri. Tu îți vezi de ziua ta; el își face treaba."),
    ("Testat în condiții reale", "Odyssey nu este un experiment de laborator. Rulează pe cont real, în condiții reale de piață, și este evaluat și îmbunătățit continuu pe baza rezultatelor obținute.")],
   ("The Odyssey Advantage", "O piață. Un robot. Zero emoții.",
    "Odyssey nu promite profituri garantate – nicio piață nu le oferă. Misiunea lui este să aducă disciplina, viteza și consecvența unui sistem automat acolo unde majoritatea traderilor pierd din cauza emoțiilor.",
    "Odyssey — Automated Discipline for the DAX.")),
  ("portfolio", "Monthly Trend Portfolio", "PORTOFOLIUL DAILY MARKET", "Răbdare. Echilibru. Transparență.",
   ["Portofoliul Daily Market este o strategie de investiții pe termen mediu, gestionată după reguli fixe și reconstruită o dată pe lună. Nu reacționează la fiecare titlu din presă și nu se lasă purtat de zgomotul zilnic. Caută direcțiile puternice ale pieței și le urmează cu răbdare."],
   [("Construit pe trenduri, nu pe zgomot", "Piețele trec prin perioade lungi de creștere și de scădere. Portofoliul identifică piețele cu direcția cea mai clară și mai stabilă și își construiește pozițiile doar acolo."),
    ("Diversificat pe mai multe clase de active", "Indici bursieri, aur, argint, petrol, valute și acțiuni de tehnologie. Portofoliul poate câștiga atât din creșteri, cât și din scăderi – nu depinde de o singură piață sau direcție."),
    ("Riscul, distribuit cu grijă", "Nicio poziție nu domină portofoliul. Piețele agitate primesc o pondere mai mică, cele liniștite o pondere mai mare. Fiecare poziție are un nivel de protecție verificat din oră în oră."),
    ("Reînnoit lunar", "La începutul fiecărei luni, portofoliul se reevaluează complet: pozițiile cu forță rămân, cele care au pierdut-o ies, iar noile oportunități își primesc locul."),
    ("Transparență totală", "Public de la prima zi. Fiecare intrare, fiecare ieșire și fiecare rezultat – câștig sau pierdere – se văd pe dailymarketlab.com. Nimic nu se ascunde și nimic nu se rescrie după rezultat.")],
   ("The Portfolio Advantage", "Mai puțină agitație. Mai multă direcție. Rezultate la vedere.",
    "Portofoliul Daily Market nu promite randamente garantate. Misiunea lui este să arate, lună de lună și la vedere, cum arată o strategie disciplinată, construită pe trendurile pieței și nu pe emoții.",
    "Daily Market Portfolio — Following the Trend, in Plain Sight.")),
 ],
 "signals": [("BUY", "O oportunitate favorabilă unei poziționări de cumpărare."), ("SELL", "O oportunitate favorabilă unei poziționări de vânzare."),
             ("SKIP", "Nicio oportunitate care să îndeplinească criteriile de selecție.")],
 "sig_title": "Un sistem intuitiv de semnale",
 "disc": "Informațiile de pe această pagină au caracter informativ și educativ și nu reprezintă consultanță de investiții sau o recomandare de a cumpăra ori vinde instrumente financiare. Tranzacționarea instrumentelor financiare, în special a celor cu efect de levier, implică un risc ridicat de pierdere a capitalului. Rezultatele trecute nu garantează rezultate viitoare.",
 "foot": '<a href="./?lang=ro">Înapoi la raport</a> · <a href="despre.html">Despre noi</a> · <a href="acuratete.html">Acuratețe</a> · <a href="termeni.html">Termeni și condiții</a> · <a href="confidentialitate.html">Confidențialitate</a> · <a href="mailto:contact@dailymarketlab.com">Contact</a> · <a href="products.html" lang="en" hreflang="en">English</a>',
 "pdf": "Descarcă broșura (PDF)",
},
"en": {
 "file": "products.html", "alt": "produse.html", "lang": "en", "home": "./",
 "title": "Our products · Daily Market", "h1": "Our <span>products</span>",
 "desc": "Athena, Odyssey and the Daily Market Portfolio: tools that turn market complexity into clear, disciplined decisions.",
 "lead": "Tools built to turn the complexity of financial markets into clear, disciplined, data-driven decisions.",
 "cta_contact": "Ask for details", "cta_pf": "See the live portfolio", "pf_url": "./#portfolio",
 "mail_subj": "Details%20about%20",
 "products": [
  ("athena", "Market Intelligence", "ATHENA", "Market Intelligence. Smarter Trading Decisions.",
   ["Athena is an intelligent financial-market analysis platform, designed to turn complex information from the options market into clear, relevant and easy-to-read signals.",
    "In a financial world where speed, volatility and information volume make the difference, Athena adds another perspective on trading opportunities, helping users make better-founded decisions."],
   [("Beyond traditional analysis", "Unlike conventional tools that focus on historical price action, Athena draws on information from the options market, combining quantitative analysis with artificial intelligence and machine learning."),
    ("Intelligence turned into action", "Athena tracks multiple financial instruments – stocks, indices, commodities and other asset classes – giving a structured, consistent view of the markets it monitors."),
    ("SIGNALS", "Every signal comes with confidence indicators, so it can be weighed against your own risk profile."),
    ("Built for markets that keep changing", "Adaptability, continuous evaluation and statistical discipline, with no reliance on subjective interpretation or emotional reactions. A modular architecture allows more instruments to be added and integration into automated workflows.")],
   ("The Athena Advantage", "Less noise. More clarity. Data-driven decisions.",
    "Athena does not promise to predict the future of financial markets. Its mission is to turn their complexity into an information edge – an additional tool for identifying, assessing and prioritising opportunities.",
    "Athena — Turning Market Complexity into Actionable Intelligence.")),
  ("odyssey", "DAX Automated Trading", "ODYSSEY", "Discipline. Precision. Consistency.",
   ["Odyssey is a fully automated trading robot dedicated to a single market: the German <b>DAX 40</b> index. It does not spread itself across dozens of instruments or chase passing fads. It does one thing – and does it with discipline, every trading day."],
   [("One market, deeply understood", "The DAX is one of Europe's most dynamic indices: fast moves, high volatility, daily opportunities. Odyssey was built exclusively for this market and tuned to its rhythm. Specialisation is its edge."),
    ("Trading without emotions", "Fear, greed, haste or the urge to win back a loss are a trader's biggest traps. Odyssey has none of them. It executes every decision by clear, consistent rules, from the first trade of the day to the last."),
    ("Capital protection comes first", "Every position has its risk defined from the moment of entry. Position size is calculated automatically, gains are protected along the way and losses are capped."),
    ("Always alert, never tired", "Odyssey watches the market without a break for the whole session and reacts in real time, without delay. You get on with your day; it gets on with the job."),
    ("Tested in real conditions", "Odyssey is not a lab experiment. It runs on a live account, in real market conditions, and is continuously evaluated and improved based on its results.")],
   ("The Odyssey Advantage", "One market. One robot. Zero emotions.",
    "Odyssey does not promise guaranteed profits – no market offers them. Its mission is to bring the discipline, speed and consistency of an automated system to where most traders lose because of emotions.",
    "Odyssey — Automated Discipline for the DAX.")),
  ("portfolio", "Monthly Trend Portfolio", "DAILY MARKET PORTFOLIO", "Patience. Balance. Transparency.",
   ["The Daily Market Portfolio is a medium-term investment strategy, run by fixed rules and rebuilt once a month. It does not react to every headline and is not carried away by daily noise. It looks for the market's strong directions and follows them patiently."],
   [("Built on trends, not noise", "Markets go through long periods of rising and falling. The portfolio identifies the markets with the clearest, most stable direction and builds its positions only there."),
    ("Diversified across asset classes", "Stock indices, gold, silver, oil, currencies and technology stocks. The portfolio can profit from rises and falls alike – it does not depend on a single market or direction."),
    ("Risk, carefully spread", "No position dominates the portfolio. Volatile markets get a smaller weight, calmer ones a larger weight. Every position has a protective level checked every hour."),
    ("Renewed every month", "At the start of each month the portfolio is fully re-assessed: strong positions stay, those that lost strength leave, and new opportunities take their place."),
    ("Full transparency", "Public from day one. Every entry, every exit and every result – win or loss – is visible on dailymarketlab.com. Nothing is hidden and nothing is rewritten after the fact.")],
   ("The Portfolio Advantage", "Less turbulence. More direction. Results in plain sight.",
    "The Daily Market Portfolio does not promise guaranteed returns. Its mission is to show, month after month and in the open, what a disciplined strategy built on market trends – not emotions – looks like.",
    "Daily Market Portfolio — Following the Trend, in Plain Sight.")),
 ],
 "signals": [("BUY", "An opportunity favouring a buy position."), ("SELL", "An opportunity favouring a sell position."),
             ("SKIP", "No opportunity meeting the selection criteria.")],
 "sig_title": "An intuitive signal system",
 "disc": "The information on this page is for information and education only and is not investment advice or a recommendation to buy or sell financial instruments. Trading financial instruments, especially leveraged ones, carries a high risk of losing capital. Past results do not guarantee future results.",
 "foot": '<a href="./">Back to the report</a> · <a href="about.html">About us</a> · <a href="accuracy.html">Accuracy</a> · <a href="terms.html">Terms &amp; conditions</a> · <a href="privacy.html">Privacy</a> · <a href="mailto:contact@dailymarketlab.com">Contact</a> · <a href="produse.html" lang="ro" hreflang="ro">Română</a>',
 "pdf": "Download the brochure (PDF)",
},
}

CSS = """
:root{--bg:#EEF1F5;--card:#fff;--ink:#13223A;--muted:#5A6B82;--line:#D5DCE6;--soft:#f6f7fb}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0C1420;--card:#131F31;--ink:#E7EDF5;--muted:#93A3B8;--line:#24344C;--soft:#1a2940}}
:root[data-theme="dark"]{--bg:#0C1420;--card:#131F31;--ink:#E7EDF5;--muted:#93A3B8;--line:#24344C;--soft:#1a2940}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Archivo',-apple-system,Segoe UI,Arial,sans-serif;font-size:16px;line-height:1.6}
header{background:#13223A}
header a{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:800;font-size:21px;font-stretch:125%;
  max-width:980px;margin:0 auto;padding:12px 16px;width:100%}
.top{background:radial-gradient(120% 90% at 85% 0%,#2a4670 0%,#13223A 55%,#0b1524 100%);color:#fff;position:relative;overflow:hidden}
.top .in{max-width:980px;margin:0 auto;padding:44px 16px 52px;position:relative}
.top .bars{position:absolute;right:24px;bottom:-6px;display:flex;align-items:flex-end;gap:16px;opacity:.85}
.top .bars i{display:block;width:34px;border-radius:8px 8px 0 0;background:linear-gradient(#E7BE6A,#B7791F)}
.top h1{font-size:clamp(34px,6vw,54px);line-height:1.05;margin:0;font-stretch:80%;letter-spacing:-.5px}
.top h1 span{color:#E7BE6A}
.top p{color:#C9D5E6;font-size:17px;max-width:56ch;margin:14px 0 0;position:relative}
.jump{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px;position:relative}
.jump a{color:#fff;text-decoration:none;font-weight:700;font-size:14px;padding:8px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.07)}
.jump a:hover{background:rgba(255,255,255,.15)}
main{max-width:980px;margin:0 auto;padding:28px 16px 40px;display:grid;gap:28px}
.prod{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;scroll-margin-top:16px}
.hero{color:#fff;padding:28px 28px 30px;position:relative}
.hero .tag{display:inline-block;font-size:11px;letter-spacing:1.8px;text-transform:uppercase;font-weight:700;padding:5px 12px;border-radius:99px;
  background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3)}
.hero h2{font-size:clamp(32px,6vw,50px);line-height:1;margin:18px 0 8px;font-weight:800;letter-spacing:-1px;font-stretch:90%;max-width:calc(100% - 120px)}
.hero .sub{font-size:17px;font-weight:600;opacity:.95}
.hero .em{position:absolute;right:28px;bottom:-34px;width:104px;height:104px;border-radius:26px;background:#fff;display:flex;align-items:center;
  justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.22)}
.hero .em svg{width:68px;height:68px}
.body{padding:30px 28px 28px}
.intro p{margin:0 0 10px;max-width:70ch;font-size:16.5px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px 28px;margin-top:18px}
.feat h3{font-size:16px;margin:0 0 4px;display:flex;gap:9px;align-items:center}
.feat h3 i{width:10px;height:10px;border-radius:3px;flex:0 0 auto}
.feat p{margin:0;color:var(--muted);font-size:15px}
.feat.wide{grid-column:1/3}
.sig{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:8px 0 10px}
.sig div{background:var(--soft);border-radius:12px;padding:12px;font-size:14px;color:var(--muted)}
.sig b{display:block;font-size:17px;margin-bottom:2px}
.adv{margin-top:24px;border-radius:14px;padding:22px 24px;color:#fff}
.adv .k{font-size:11px;letter-spacing:1.8px;text-transform:uppercase;font-weight:700;opacity:.85}
.adv .t{font-size:clamp(19px,3vw,23px);font-weight:800;margin-top:4px;line-height:1.25}
.adv p{margin:8px 0 0;opacity:.93;font-size:15px}
.adv .s{font-style:italic;font-weight:600;margin-top:10px;opacity:.95}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.cta a{display:inline-block;text-decoration:none;font-weight:700;font-size:15px;padding:11px 18px;border-radius:10px;color:#fff}
.athena .hero,.athena .adv,.athena .cta a{background:linear-gradient(135deg,#3b1f78 0%,#5b3fc4 60%,#8a6cf0 100%)} .athena i{background:#6d4fe0}
.odyssey .hero,.odyssey .adv,.odyssey .cta a{background:linear-gradient(135deg,#053b4a 0%,#0b6e80 60%,#1fb3b0 100%)} .odyssey i{background:#0e9aa0}
.portfolio .hero{background:linear-gradient(135deg,#13223A 0%,#2a4670 55%,#B7791F 140%)}
.portfolio .adv,.portfolio .cta a{background:linear-gradient(135deg,#13223A,#2a4670)} .portfolio i{background:#D9A441}
.pdf{text-align:center}
.pdf a{display:inline-block;font-weight:700;color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--card);padding:11px 20px;border-radius:10px}
.disc{color:var(--muted);font-size:13px;max-width:none}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:13px}
footer div{max-width:980px;margin:0 auto;padding:18px 16px 32px}
footer a{color:inherit}
@media (max-width:640px){
  .grid,.sig{grid-template-columns:1fr}.feat.wide{grid-column:auto}
  .hero{padding:22px 18px 26px}.body{padding:26px 18px 22px}
  .hero .em{width:76px;height:76px;border-radius:20px;right:18px;bottom:-26px}.hero .em svg{width:48px;height:48px}
  .hero h2{max-width:calc(100% - 80px)}
  .top .bars{opacity:.35}
}
"""


def page(lang: str) -> str:
    t = T[lang]
    secs, jump = [], []
    for key, tag, name, sub, intro, feats, adv in t["products"]:
        jump.append(f'<a href="#{key}">{name.title() if key != "portfolio" else name.split()[0].title() if lang == "ro" else "Portfolio"}</a>')
        fh = []
        for h, p in feats:
            if h == "SIGNALS":
                cols = {"BUY": "#15803d", "SELL": "#c2362f", "SKIP": "#6b7280"}
                sig = "".join(f'<div><b style="color:{cols[k]}">{k}</b>{v}</div>' for k, v in t["signals"])
                fh.append(f'<div class="feat wide"><h3><i></i>{t["sig_title"]}</h3><div class="sig">{sig}</div><p>{p}</p></div>')
            else:
                wide = " wide" if (feats.index((h, p)) == len(feats) - 1 and len(feats) % 2 == 1) else ""
                fh.append(f'<div class="feat{wide}"><h3><i></i>{h}</h3><p>{p}</p></div>')
        if key == "portfolio":
            cta = f'<a href="{t["pf_url"]}">{t["cta_pf"]}</a>'
        else:
            cta = f'<a href="mailto:contact@dailymarketlab.com?subject={t["mail_subj"]}{name.title()}">{t["cta_contact"]}</a>'
        secs.append(f"""<section class="prod {key}" id="{key}">
<div class="hero"><span class="tag">{tag}</span><h2>{name}</h2><div class="sub">{sub}</div><div class="em">{EMBLEM[key]}</div></div>
<div class="body"><div class="intro">{''.join(f'<p>{x}</p>' for x in intro)}</div>
<div class="grid">{''.join(fh)}</div>
<div class="adv"><div class="k">{adv[0]}</div><div class="t">{adv[1]}</div><p>{adv[2]}</p><div class="s">{adv[3]}</div></div>
<div class="cta">{cta}</div></div></section>""")
    other = "en" if lang == "ro" else "ro"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}">
<link rel="canonical" href="https://dailymarketlab.com/{t["file"]}">
<link rel="alternate" hreflang="{lang}" href="https://dailymarketlab.com/{t["file"]}">
<link rel="alternate" hreflang="{other}" href="https://dailymarketlab.com/{t["alt"]}">
<meta property="og:title" content="{t["title"]}"><meta property="og:description" content="{t["desc"]}">
<meta property="og:image" content="https://dailymarketlab.com/og.png">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script src="/ga.js" defer></script>
</head>
<body>
<header><a href="{t["home"]}">{LOGO.format(s=26)}Daily Market</a></header>
<div class="top"><div class="bars"><i style="height:70px"></i><i style="height:120px"></i><i style="height:46px"></i></div>
<div class="in"><h1>{t["h1"]}</h1><p>{t["lead"]}</p><div class="jump">{''.join(jump)}</div></div></div>
<main>
{''.join(secs)}
<div class="pdf"><a href="Daily-Market-Produse.pdf" download>⬇ {t["pdf"]}</a></div>
<p class="disc">{t["disc"]}</p>
</main>
<footer><div>{t["foot"]}</div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    for lg in ("ro", "en"):
        (here / T[lg]["file"]).write_text(page(lg), encoding="utf-8")
        print("scris", T[lg]["file"])
