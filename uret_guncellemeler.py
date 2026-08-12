# -*- coding: utf-8 -*-
"""guncellemeler.html'i urunlerin CHANGELOG.md dosyalarindan URETIR.
Elle duzenlenmez - kaynak her urunun 07_surum_gecmisi/CHANGELOG.md dosyasidir."""
import os, re, html
from datetime import datetime
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent          # 02_ticaret
WEB = KOK / "05_web"
MS  = KOK / "01_microsoft_store"

URUNLER = [
 ("USUL365 Guard",       "guard.png",       MS/"01_USUL365_Guard/07_surum_gecmisi/CHANGELOG.md",        "/uygulamalar/guard/"),
 ("USUL365 Namaz Vakti", "namaz-vakti.png", MS/"03_USUL365_NamazVakti/07_surum_gecmisi/CHANGELOG.md",   "/uygulamalar/namaz-vakti/"),
 ("USUL365 HesapPro",    "hesappro.png",    MS/"02_USUL365_HesapPro/07_surum_gecmisi/CHANGELOG.md",     "/#uygulamalar"),
 ("Blok Düşür",          "blok.png",        MS/"OYUNLAR/01_USUL365_Blok/07_surum_gecmisi/CHANGELOG.md", "/oyunlar/blok-dusur/"),
]

def ayikla(yol):
    """## baslik + madde listesi -> [(baslik, [madde,...])]"""
    if not yol.exists(): return None
    surumler, simdiki = [], None
    for s in yol.read_text(encoding="utf-8", errors="replace").splitlines():
        s = s.rstrip()
        if s.startswith("## "):
            simdiki = (s[3:].strip(), [])
            surumler.append(simdiki)
        elif s.startswith("- ") and simdiki:
            simdiki[1].append(s[2:].strip())
    return surumler

parca, bulunan, eksik = [], 0, []
for ad, ikon, yol, bag in URUNLER:
    sur = ayikla(yol)
    if not sur:
        eksik.append((ad, yol)); continue
    bulunan += 1
    satirlar = []
    for baslik, maddeler in sur:
        md = "".join("<li>%s</li>" % html.escape(m) for m in maddeler)
        satirlar.append('<div class="surum"><div class="sbas">%s</div><ul>%s</ul></div>'
                        % (html.escape(baslik), md))
    parca.append(
      '<section class="urunblok">'
      '<div class="ubas"><div class="uikon"><img src="/ikonlar/%s" alt=""></div>'
      '<div><span class="uad">%s</span>'
      '<a class="ubag" href="%s">Ürün sayfası &#8594;</a></div></div>%s</section>'
      % (ikon, html.escape(ad), bag, "".join(satirlar)))

SAYFA = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>Güncellemeler — USUL365</title>
<meta name="description" content="USUL365 ürünlerinin sürüm geçmişi: her sürümde neyin değiştiği.">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/ortak.css">
<style>
:root{--bg:#FAF8F3;--kart:#FFF;--cizgi:#EAE4D8;--metin:#2B2B2B;--soluk:#8A8A8A;--altin:#C9A227;--mavi:#4A6FA5}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--metin);font-family:"Segoe UI",system-ui,sans-serif;line-height:1.6}
.en{max-width:1080px;margin:0 auto;padding:0 24px}
.hero{padding:60px 0 34px;border-bottom:1px solid var(--cizgi)}
.hero .kucuk{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:2px;
  text-transform:uppercase;color:var(--altin);margin-bottom:14px}
.hero h1{font-size:34px;margin:0 0 14px;letter-spacing:-.5px}
.hero p{font-size:16.5px;color:#5A5A5A;margin:0;max-width:62ch}
.urunblok{padding:40px 0;border-bottom:1px solid var(--cizgi)}
.urunblok .ubas{display:flex;align-items:center;gap:13px;margin-bottom:20px}
.uikon{width:42px;height:42px;flex:0 0 42px;border-radius:11px;background:#fff;
  border:1px solid var(--cizgi);padding:5px}
.uikon img{width:100%;height:100%;object-fit:contain;display:block}
.uad{font-weight:600;font-size:17px;display:block}
.ubag{font-size:12.5px;color:var(--mavi);text-decoration:none}
.surum{background:var(--kart);border:1px solid var(--cizgi);border-radius:14px;
  padding:18px 22px;margin-bottom:12px}
.sbas{font-family:"Space Mono",monospace;font-size:12.5px;letter-spacing:.6px;
  color:var(--metin);font-weight:700;margin-bottom:8px}
.surum ul{margin:0;padding-left:20px}
.surum li{font-size:14px;color:#5A5A5A;margin-bottom:4px}
.uretim{padding:26px 0 10px;font-family:"Space Mono",monospace;font-size:11px;color:var(--soluk)}
</style>
</head>
<body>
<div class="en">
  <section class="hero">
    <div class="kucuk">Güncellemeler</div>
    <h1>Her sürümde ne değişti</h1>
    <p>USUL365 ürünleri yayımlandıktan sonra geliştirilmeye devam eder. Aşağıda her
       ürünün sürüm geçmişi ve o sürümde yapılan değişiklikler yer alır. Güncellemeler
       Microsoft Store üzerinden ücretsiz ulaşır.</p>
  </section>
  __ICERIK__
  <div class="uretim">Bu sayfa ürün sürüm kayıtlarından otomatik üretilir · Son üretim: __TARIH__</div>
</div>
<script src="/ortak.js"></script>
</body>
</html>
'''
SAYFA = SAYFA.replace("__ICERIK__", "\n".join(parca))
SAYFA = SAYFA.replace("__TARIH__", datetime.now().strftime("%d.%m.%Y %H:%M"))
(WEB / "guncellemeler.html").write_text(SAYFA, encoding="utf-8")

print("guncellemeler.html uretildi -", (WEB/"guncellemeler.html").stat().st_size, "bayt")
print("Sürüm geçmişi bulunan ürün:", bulunan)
for ad, yol in eksik:
    print("  CHANGELOG YOK:", ad, "->", yol.relative_to(KOK))
