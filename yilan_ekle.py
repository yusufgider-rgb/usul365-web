import json, io
y = r"icerik\urunler.json"
d = json.load(io.open(y, encoding="utf-8"))
slugs = [u["slug"] for u in d["urunler"]]

if "yilan" not in slugs:
    d["urunler"].append({
      "slug": "yilan", "ad": "Yılan", "etiket": "TARAYICI OYUNU",
      "ikon": "blok.png", "storeId": "", "fiyat": "Ücretsiz", "surum": "",
      "tur": "oyun", "sayfa": "/oyunlar/yilan/", "oyunBag": "/oyunlar/yilan/",
      "kisa": "Klasik yılan oyunu. Kurulum gerektirmez, doğrudan tarayıcıda çalışır.",
      "ozellikler": []
    })
    print("Yilan eklendi")
else:
    print("Yilan zaten var")

json.dump(d, io.open(y, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for u in d["urunler"]:
    print("  %-13s tur=%-9s store=%-14s oyunBag=%s" % (
        u["slug"], u["tur"], u.get("storeId") or "-", u.get("oyunBag") or "-"))
