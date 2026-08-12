# -*- coding: utf-8 -*-
"""USUL365 site ureticisi. Sayfalar ELLE YAZILMAZ.
Kaynak: icerik/urunler.json + her urunun 07_surum_gecmisi/CHANGELOG.md + VERSION.txt
Calistirma: python uret_site.py"""
import json, html, re
from datetime import datetime
from pathlib import Path

WEB = Path(__file__).resolve().parent
MS  = WEB.parent / "01_microsoft_store"
SUR = {"guard":       MS/"01_USUL365_Guard/07_surum_gecmisi",
       "hesappro":    MS/"02_USUL365_HesapPro/07_surum_gecmisi",
       "namaz-vakti": MS/"03_USUL365_NamazVakti/07_surum_gecmisi",
       "blok-dusur":  MS/"OYUNLAR/01_USUL365_Blok/07_surum_gecmisi"}

D = json.loads((WEB/"icerik/urunler.json").read_text(encoding="utf-8"))
M, U = D["marka"], D["urunler"]
e, Z = html.escape, datetime.now().strftime("%d.%m.%Y %H:%M")

def changelog(s):
    y = SUR.get(s, Path("/yok"))/"CHANGELOG.md"
    if not y.exists(): return []
    out, cur = [], None
    for r in y.read_text(encoding="utf-8", errors="replace").splitlines():
        r = r.rstrip()
        if r.startswith("## "): cur = (r[3:].strip(), []); out.append(cur)
        elif r.startswith("- ") and cur: cur[1].append(r[2:].strip())
    return out

def surum(s, vars):
    y = SUR.get(s, Path("/yok"))/"VERSION.txt"
    if y.exists():
        m = re.search(r"\b(\d+\.\d+\.\d+(?:\.\d+)?)\b", y.read_text(encoding="utf-8", errors="replace"))
        if m: return m.group(1)
    return vars or ""

def gorseller(s):
    k = WEB/"uygulamalar"/s/"gorseller"
    return sorted(f.name for f in k.iterdir() if f.suffix.lower() in (".png",".jpg",".jpeg")) if k.exists() else []

def store(u, cid):
    return "https://apps.microsoft.com/detail/%s?hl=tr-TR&amp;gl=TR&amp;cid=%s" % (u["storeId"], cid)

BAS = ('<!DOCTYPE html>\n<html lang="tr"><head>\n<meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
 '<link rel="icon" href="/favicon.ico" sizes="any">'
 '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<title>%s</title>'
 '<meta name="description" content="%s">\n'
 '<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">\n'
 '<link rel="stylesheet" href="/ortak.css"><link rel="stylesheet" href="/site.css">\n</head><body>')
SON = '<script src="/ortak.js"></script></body></html>'

def yaz(yol, s):
    p = WEB/yol; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8"); print("  %-42s %6d bayt" % (yol, len(s.encode())))

def kart(u, tarayici=False):
    v = surum(u["slug"], u.get("surum"))
    vt = (" &middot; v" + e(v)) if v else ""
    if tarayici:
        bag = '<a href="%s">Oyna &#8594;</a>' % u["oyunBag"]
    else:
        bag = '<a href="%s">%s &#8594;</a>' % (u["sayfa"], "Ürünü tanıyın")
        if u.get("storeId"):
            bag += ('<a class="ikincil" id="lnk-%s" href="%s" target="_blank" rel="noopener">Microsoft Store</a>'
                    % (u["slug"], store(u, "site_anasayfa")))
    return ('<div class="urun"><div class="ubas"><div class="uikon"><img src="/ikonlar/%s" alt=""></div>'
      '<div><span class="uad">%s</span><span class="uetiket">%s%s</span></div></div>'
      '<p class="uaciklama">%s</p><div class="ubaglar">%s</div>'
      '<span class="sayac" id="stat-%s"></span></div>'
      % (u["ikon"], e(u["ad"]), e(u["etiket"]), vt, e(u["kisa"]), bag, u["slug"]))

def bolum(bid, baslik, aciklama, kartlar):
    return ('<section class="bolum" id="%s"><h2>%s</h2><p class="aciklama">%s</p>'
            '<div class="izgara">%s</div></section>' % (bid, baslik, aciklama, kartlar))

# --- ANA SAYFA ---
uyg   = [u for u in U if u["tur"] == "uygulama"]
oyunS = [u for u in U if u["tur"] == "oyun" and u.get("storeId")]
oyunT = [u for u in U if u["tur"] == "oyun" and u.get("oyunBag")]
ilke = "".join('<div class="ilke"><h3>%s</h3><p>%s</p></div>' % (e(i["b"]), e(i["a"])) for i in M["ilkeler"])
yaz("index.html", BAS % (e(M["ad"])+" — "+e(M["baslik"]), e(M["girisMetni"][:150])) +
 '<div class="en"><section class="hero"><div class="kucuk">%s</div><h1>%s</h1><p>%s</p></section>'
 '<section class="ilkeler">%s</section>%s%s%s</div>'
 % (e(M["ustetiket"]), e(M["baslik"]), e(M["girisMetni"]), ilke,
    bolum("uygulamalar", "Uygulamalar", "Microsoft Store üzerinden dağıtılan masaüstü uygulamaları.",
          "".join(kart(u) for u in uyg)),
    bolum("oyunlar", "Oyunlar &mdash; Microsoft Store", "Windows için indirilebilir oyunlar.",
          "".join(kart(u) for u in oyunS)),
    bolum("playables", "Google Playables", "Tarayıcıda doğrudan oynanan sürümler; Google Playables için hazırlanıyor.",
          "".join(kart(u, True) for u in oyunT))) + SON)

# --- URUN SAYFALARI ---
for u in U:
    if not u["ozellikler"]: continue
    v = surum(u["slug"], u.get("surum"))
    oz = "".join('<div class="oz"><b>%s</b><span>%s</span></div>' % (e(o["b"]), e(o["a"])) for o in u["ozellikler"])
    _ac = {x["d"]: x["a"] for x in u.get("gorseller", [])}
    gor = "".join('<figure><img src="gorseller/%s" alt="%s"><figcaption>%s</figcaption></figure>'
                  % (g, e(u["ad"]), e(_ac.get(g, ""))) for g in gorseller(u["slug"]))
    cl = changelog(u["slug"])
    sur = "".join('<div class="surum"><div class="sbas">%s</div><ul>%s</ul></div>'
                  % (e(b), "".join("<li>%s</li>" % e(x) for x in ml)) for b, ml in cl[:3])
    btn = []
    if u.get("storeId"):
        btn.append('<a class="dbtn" href="%s" target="_blank" rel="noopener">Microsoft Store&#39;da %s</a>'
                   % (store(u, "site_"+u["slug"]), "edinin" if u["fiyat"] != "Ücretsiz" else "ücretsiz indirin"))
    if u.get("oyunBag"):
        btn.append('<a class="dbtn ikinci" href="%s">Tarayıcıda oyna</a>' % u["oyunBag"])
    if (WEB/"uygulamalar"/u["slug"]/"yardim.html").exists():
        btn.append('<a class="dbtn ikinci" href="yardim.html">Kullanım kılavuzu</a>')
    yaz("uygulamalar/%s/index.html" % u["slug"], BAS % (e(u["ad"])+" — USUL365", e(u["kisa"][:150])) +
      '<div class="en"><section class="hero"><div class="kucuk">%s%s</div><h1>%s</h1><p>%s</p>'
      '<div class="dbtnler">%s</div></section>'
      '<section class="bolum"><h2>Ne sunuyor</h2><div class="izgara3">%s</div></section>%s%s</div>'
      % (e(u["etiket"]), (" &middot; v"+e(v)) if v else "", e(u["ad"]), e(u["kisa"]), "".join(btn), oz,
         ('<section class="bolum"><h2>Ekran görüntüleri</h2>%s</section>' % gor) if gor else "",
         ('<section class="bolum"><h2>Son güncellemeler</h2>%s<p class="aciklama" style="margin-top:14px">'
          '<a href="/guncellemeler.html">Tüm sürüm geçmişi &#8594;</a></p></section>' % sur) if sur else "")
      + SON)

# --- KURUMSAL ---
kutu = "".join('<div class="oz"><b>%s</b><span>%s</span></div>' % (e(i["b"]), e(i["a"])) for i in M["ilkeler"])
yaz("kurumsal.html", BAS % ("Kurumsal — USUL365", "USUL365 hakkında: yaklaşım, ilkeler, dağıtım ve destek.") +
 '<div class="en"><section class="hero"><div class="kucuk">Kurumsal</div>'
 '<h1>USUL365 hakkında</h1><p>%s</p></section>'
 '<section class="bolum"><h2>Ne yapıyoruz</h2>'
 '<p class="aciklama">Günlük kullanımda gerçekten ihtiyaç duyulan, tek bir işi düzgün yapan '
 'yazılımlar geliştiriyoruz. Az sayıda özelliğin eksiksiz çalışmasını, çok sayıda özelliğin '
 'yarım kalmasına tercih ediyoruz. Ürünler yayımlandıktan sonra bırakılmaz; tespit edilen '
 'kusurlar ve gelen geri bildirimler sonraki sürümlere girer.</p>'
 '<p class="aciklama">Doğruluk gerektiren veriler resmî kaynaklarıyla karşılaştırılarak doğrulanır. '
 'Örneğin namaz vakitleri ve hicrî takvim, Diyanet İşleri Başkanlığının yayımladığı resmî '
 'takvimden okunur; hesaplamaya bırakılmaz.</p>'
 '<p class="aciklama">Geliştirme hattımız yapay zekâ destekli çalışır: içerik üretimi, kaynak '
 'karşılaştırması ve denetim adımları bu hat üzerinde yürür. Bugün Windows üzerindeyiz; '
 'sırada Google Play ve Apple platformları var.</p></section>'
 '<section class="bolum"><h2>İlkelerimiz</h2><div class="izgara3">%s</div></section>'
 '<section class="bolum"><h2>Dağıtım ve destek</h2>'
 '<p class="aciklama">Masaüstü ürünleri Microsoft Store üzerinden dağıtılır; paketler Microsoft '
 'tarafından imzalanır ve sertifikasyondan geçer. Soru, hata bildirimi ve öneriler için '
 '<a href="mailto:%s">%s</a> adresine yazabilirsiniz.</p></section></div>'
 % (e(M["girisMetni"]), kutu, M["eposta"], M["eposta"]) + SON)

# --- GUNCELLEMELER ---
blok = []
for u in U:
    cl = changelog(u["slug"])
    if not cl: continue
    sur = "".join('<div class="surum"><div class="sbas">%s</div><ul>%s</ul></div>'
                  % (e(b), "".join("<li>%s</li>" % e(x) for x in ml)) for b, ml in cl)
    blok.append('<section class="bolum"><div class="ubas"><div class="uikon">'
                '<img src="/ikonlar/%s" alt=""></div><div><span class="uad">%s</span>'
                '<a class="ubag" href="%s">Ürün sayfası &#8594;</a></div></div>%s</section>'
                % (u["ikon"], e(u["ad"]), u["sayfa"], sur))
yaz("guncellemeler.html", BAS % ("Güncellemeler — USUL365", "USUL365 ürünlerinin sürüm geçmişi.") +
 '<div class="en"><section class="hero"><div class="kucuk">Güncellemeler</div>'
 '<h1>Her sürümde ne değişti</h1><p>Ürünler yayımlandıktan sonra geliştirilmeye devam eder. '
 'Bu sayfa ürünlerin kendi sürüm kayıtlarından otomatik üretilir.</p></section>%s'
 '<div class="uretim">Son üretim: %s</div></div>'
 % ("".join(blok) or "<p>Henüz sürüm kaydı yok.</p>", Z) + SON)

print("\nTAMAM -", Z)
