/* Daily Market – Google Analytics 4 și pixelul Meta, cu consimțământ (Consent Mode v2).
   Implicit totul e refuzat: GA și Meta nu pun cookie-uri până când vizitatorul nu apasă „Accept”.
   Pixelul Meta (2331828450722469) măsoară doar dacă reclamele noastre de pe Facebook aduc abonați (PageView + Lead).
   Alegerea se ține în localStorage (dm_consent = "yes" | "no"). ?nostat=1 oprește tot pe acel aparat. */
(function () {
  var GA_ID = "G-BCF4V2ZZ56", FB_PIXEL = "2331828450722469", CONSENT_V = "2";   // v2 = textul care pomenește și Meta
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  if (get("dm_nostat") === "1") return;

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  var choice = get("dm_consent");
  var fresh = get("dm_consent_v") === CONSENT_V;   // alegerea a fost făcută pe textul actual?
  function fb() {   // pixelul Meta: se încarcă doar după „Accept”
    if (window.fbq) return;
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", FB_PIXEL); window.fbq("track", "PageView");
  }
  // abonare reușită -> eveniment „Lead” (doar dacă vizitatorul a acceptat)
  window.dmLead = function () { try { if (window.fbq) window.fbq("track", "Lead"); } catch (e) {} };
  if (choice === "yes" && fresh) fb();
  gtag("consent", "default", {
    ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied",
    analytics_storage: choice === "yes" ? "granted" : "denied", wait_for_update: 500
  });
  gtag("set", "ads_data_redaction", true);
  gtag("js", new Date());
  gtag("config", GA_ID, { anonymize_ip: true });
  var s = document.createElement("script");
  s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(s);

  function ro() { return (document.documentElement.lang || "").slice(0, 2) === "ro"; }
  function decide(yes) {
    set("dm_consent", yes ? "yes" : "no"); set("dm_consent_v", CONSENT_V);
    gtag("consent", "update", { analytics_storage: yes ? "granted" : "denied" });
    if (yes) fb();
    var b = document.getElementById("dmCookie"); if (b) b.remove();
  }
  function banner() {
    if (document.getElementById("dmCookie")) return;
    var r = ro(), d = document.createElement("div");
    d.id = "dmCookie"; d.setAttribute("role", "dialog");
    d.setAttribute("aria-label", r ? "Cookie-uri" : "Cookies");
    d.style.cssText = "position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:560px;margin:0 auto;" +
      "background:#14171c;color:#eef0f3;border:1px solid #2c323b;border-radius:12px;padding:14px 16px;" +
      "font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.35)";
    var priv = r ? "/confidentialitate.html" : "/privacy.html";
    d.innerHTML = '<div style="margin-bottom:10px">' + (r
      ? 'Folosim Google Analytics ca să vedem câți oameni citesc Daily Market și pixelul Meta (Facebook) ca să știm dacă reclamele noastre aduc abonați. Pun cookie-uri doar dacă accepți. <a href="' + priv + '" style="color:#7cb7ff">Detalii</a>'
      : 'We use Google Analytics to see how many people read Daily Market and the Meta (Facebook) pixel to know whether our ads bring subscribers. They only set cookies if you accept. <a href="' + priv + '" style="color:#7cb7ff">Details</a>') +
      '</div><div style="display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap">' +
      '<button type="button" data-v="0" style="padding:8px 14px;border-radius:8px;border:1px solid #3a414c;background:transparent;color:#eef0f3;font:inherit;cursor:pointer">' + (r ? "Refuz" : "Decline") + '</button>' +
      '<button type="button" data-v="1" style="padding:8px 14px;border-radius:8px;border:0;background:#2f7cf6;color:#fff;font:inherit;font-weight:600;cursor:pointer">' + (r ? "Accept" : "Accept") + '</button></div>';
    d.addEventListener("click", function (e) {
      var v = e.target && e.target.getAttribute && e.target.getAttribute("data-v");
      if (v !== null && v !== undefined) decide(v === "1");
    });
    document.body.appendChild(d);
  }
  window.dmCookieSettings = banner;
  try {  // dacă pagina își schimbă limba (butonul RO/EN), refac textul bannerului
    new MutationObserver(function () {
      var b = document.getElementById("dmCookie"); if (b) { b.remove(); banner(); }
    }).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  } catch (e) {}  // linkul „Setări cookie-uri” redeschide bannerul
  if ((choice !== "yes" && choice !== "no") || (choice === "yes" && !fresh)) {   // cine a acceptat textul vechi e întrebat din nou
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", banner); else banner();
  }
})();
