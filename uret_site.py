# -*- coding: utf-8 -*-
"""USUL365 site ureticisi. Sayfalar ELLE YAZILMAZ - bu betik uretir.
Kaynaklar: icerik/urunler.json  +  her urunun 07_surum_gecmisi/CHANGELOG.md
Calistirma: python uret_site.py"""
import json, html, os
from datetime import datetime
from pathlib import Path

WEB = Path(__file__).resolve().parent
KOK = WEB.parent
MS  = KOK / "01_microsoft_store"
SURUM_YOL = {
 "guard":       MS/"01_USUL365_Guard/07_surum_gecmisi",
 "hesappro":    MS/"02_USUL365_HesapPro/07_surum_gecmisi",
 "namaz-vakti": MS/"03_USUL365_NamazVakti/07_surum_gecmisi",
 "blok-dusur":  MS/"OYUNLAR/01_USUL365_Blok/07_surum_gecmisi",
}
D = json.loads((WEB/"icerik/urunler.json").read_text(encoding="utf-8"))
M, U = D["marka"], D["urunler"]
e = html.escape
Z = datetime.now().strftime("%d.%m.%Y %H:%M")

def changelog(slug):
    y = SURUM_YOL.get(slug, Path("/yok")) / "CHANGELOG.md"
    if not y.exists(): return []
    out, cur = [], None
    for s in y.read_text(encoding="utf-8", errors="replace").splitlines():
        s = s.rstrip()
        if s.startswith("## "): cur = (s[3:].strip(), []); out.append(cur)
        elif s.startswith("- ") and cur: cur[1].append(s[2:].strip())
    return out

def surum(slug, vars):
    y = SURUM_YOL.get(slug, Path("/yok")) / "VERSION.txt"
    if y.exists():
        v = y.read_text(encoding="utf-8").strip()
        if v: return v
    return vars

def gorseller(slug):
    k = WEB/"uygulamalar"/slug/"gorseller"
    if not k.exists(): return []
    return sorted(f.name for f in k.iterdir() if f.suffix.lower() in (".png",".jpg",".jpeg"))

def store(u, cid):
    return "https://apps.microsoft.com/detail/%s?hl=tr-TR&amp;gl=TR&amp;cid=%s" % (u["storeId"], cid)

BAS = '''<!DOCTYPE html>
<html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>%s</title><meta name="description" content="%s">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/ortak.css"><link rel="stylesheet" href="/site.css">
</head><body>'''
SON = '<script src="/ortak.js"></script></body></html>'

def yaz(yol, icerik):
    p = WEB/yol; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(icerik, encoding="utf-8"); print("  uretildi: %-44s %6d bayt" % (yol, len(icerik.encode())))

# ---------- ANA SAYFA ----------
kart = []
for u in U:
    v = surum(u["slug"], u.get("surum",""))
    ana = u.get("oyunBag") or u["sayfa"]
    kart.append(
      '<div class="urun"><div class="ubas"><div class="uikon"><img src="/ikonlar/%s" alt=""></div>'
      '<div><span class="uad">%s</span><span class="uetiket">%s · v%s</span></div></div>'
      '<p class="uaciklama">%s</p><div class="ubaglar">'
      '<a href="%s">Ürünü tanıyın &#8594;</a>'
      '<a class="ikincil" id="lnk-%s" href="%s" target="_blank" rel="noopener">%s</a>'
      '</div><span class="sayac" id="stat-%s"></span></div>'
      % (u["ikon"], e(u["ad"]), e(u["etiket"]), e(v), e(u["kisa"]), u["sayfa"],
         u["slug"], store(u,"site_anasayfa"),
         "Tarayıcıda oyna" if u.get("oyunBag") else "Microsoft Store", u["slug"]))
ilke = "".join('<div class="ilke"><h3>%s</h3><p>%s</p></div>' % (e(i["b"]), e(i["a"])) for i in M["ilkeler"])
yaz("index.html", BAS % (e(M["ad"])+" — "+e(M["baslik"]), e(M["girisMetni"][:150])) +
 '<div class="en"><section class="hero"><div class="kucuk">%s</div><h1>%s</h1><p>%s</p></section>'
 '<section class="ilkeler">%s</section>'
 '<section class="bolum" id="uygulamalar"><h2>Ürünler</h2>'
 '<p class="aciklama">Microsoft Store üzerinden dağıtılan uygulama ve oyunlar.</p>'
 '<div class="izgara">%s</div></section></div>'
 % (e(M["ustetiket"]), e(M["baslik"]), e(M["girisMetni"]), ilke, "".join(kart)) + SON)

# ---------- URUN SAYFALARI ----------
for u in U:
    v = surum(u["slug"], u.get("surum",""))
    oz = "".join('<div class="oz"><b>%s</b><span>%s</span></div>' % (e(o["b"]), e(o["a"])) for o in u["ozellikler"])
    gor = "".join('<figure><img src="gorseller/%s" alt="%s"></figure>' % (g, e(u["ad"])) for g in gorseller(u["slug"]))
    cl = changelog(u["slug"])
    sur = "".join('<div class="surum"><div class="sbas">%s</div><ul>%s</ul></div>'
                  % (e(b), "".join("<li>%s</li>" % e(m) for m in ml)) for b, ml in cl[:3])
    ek = ('<a class="dbtn ikinci" href="%s">Tarayıcıda oyna</a>' % u["oyunBag"]) if u.get("oyunBag") else ""
    yrd = "yardim.html" if (WEB/"uygulamalar"/u["slug"]/"yardim.html").exists() else ""
    yaz("uygulamalar/%s/index.html" % u["slug"],
      BAS % (e(u["ad"]) + " — USUL365", e(u["kisa"][:150])) +
      '<div class="en"><section class="hero"><div class="kucuk">%s · v%s</div><h1>%s</h1>'
      '<p>%s</p><div class="dbtnler">'
      '<a class="dbtn" href="%s" target="_blank" rel="noopener">Microsoft Store\'da %s</a>%s%s</div></section>'
      '<section class="bolum"><h2>Ne sunuyor</h2><div class="izgara3">%s</div></section>'
      '%s%s</div>'
      % (e(u["etiket"]), e(v), e(u["ad"]), e(u["kisa"]), store(u,"site_"+u["slug"]),
         "edinin" if u["fiyat"] != "Ücretsiz" else "ücretsiz indirin", ek,
         ('<a class="dbtn ikinci" href="%s">Kullanım kılavuzu</a>' % yrd) if yrd else "",
         oz,
         ('<section class="bolum"><h2>Ekran görüntüleri</h2>%s</section>' % gor) if gor else "",
         ('<section class="bolum"><h2>Son güncellemeler</h2>%s'
          '<p class="aciklama" style="margin-top:14px"><a href="/guncellemeler.html">Tüm sürüm geçmişi &#8594;</a></p></section>' % sur) if sur else "")
      + SON)

# ---------- GUNCELLEMELER ----------
blok = []
for u in U:
    cl = changelog(u["slug"])
    if not cl: continue
    sur = "".join('<div class="surum"><div class="sbas">%s</div><ul>%s</ul></div>'
                  % (e(b), "".join("<li>%s</li>" % e(m) for m in ml)) for b, ml in cl)
    blok.append('<section class="bolum"><div class="ubas"><div class="uikon"><img src="/ikonlar/%s" alt=""></div>'
                '<div><span class="uad">%s</span><a class="ubag" href="%s">Ürün sayfası &#8594;</a></div></div>%s</section>'
                % (u["ikon"], e(u["ad"]), u["sayfa"], sur))
yaz("guncellemeler.html", BAS % ("Güncellemeler — USUL365", "USUL365 ürünlerinin sürüm geçmişi.") +
 '<div class="en"><section class="hero"><div class="kucuk">Güncellemeler</div>'
 '<h1>Her sürümde ne değişti</h1><p>Ürünler yayımlandıktan sonra geliştirilmeye devam eder. '
 'Bu sayfa ürünlerin kendi sürüm kayıtlarından otomatik üretilir.</p></section>%s'
 '<div class="uretim">Son üretim: %s</div></div>' % ("".join(blok) or "<p>Henüz sürüm kaydı yok.</p>", Z) + SON)

print("\nTAMAM -", Z)
