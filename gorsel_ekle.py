import json, io
y = r"icerik\urunler.json"
d = json.load(io.open(y, encoding="utf-8"))

G = {
 "guard": [["usul365_guard_ekran_gorutusu_1.png",
   "Genel Bakış ekranı: sistem skoru ve alt başlıklar (program yükü, disk sağlığı, güvenlik, kaynaklar) tek listede, en zayıf halka en üstte."]],
 "namaz-vakti": [
   ["01_genis_gorunum.png", "Geniş görünüm: solda vakit listesi ve geri sayım, sağda günün ayeti, yaklaşan dinî günler ve hicrî takvim."],
   ["02_sade_gorunum.png",  "Sade görünüm: yalnız vakitler ve kalan süre; ekranda az yer kaplaması istendiğinde."],
   ["03_ne_sunuyor.png",    "Haftalık tablo: tarih, gün adı ve hicrî karşılığıyla birlikte yedi günün vakitleri."],
   ["04_nasil_calisir.png", "Bilgi sekmesi: kıble açısı, Kâbe mesafesi, astronomik doğuş-batış ve uygulama sürümü."]],
 "hesappro": [
   ["01_standart_tr_1366.png", "Standart mod, Türkçe arayüz: temel hesaplama ve İş & Finans sekmesi."],
   ["02_english_1366.png",     "Aynı ekran İngilizce arayüzde; dil değişimi anında uygulanır."],
   ["04_arabic_1366.png",      "Arapça arayüz: sayı ve düğme yerleşimi dile göre uyarlanır."]],
 "blok-dusur": [
   ["blok_01_oyun_ici.png",  "Oyun ekranı: skor, seviye, satır sayısı ve sıradaki blok yan panelde."],
   ["blok_02_menu.png",      "Başlangıç menüsü: zorluk seçimi ve seviye bazlı liderlik tablosu."],
   ["blok_03_diller.png",    "Dil menüsü: on dil arasında anında geçiş."],
   ["blok_04_istatistik.png","İstatistikler: oynanan oyun, toplam satır ve seviye bazlı rekorlar."]],
}
for u in d["urunler"]:
    if u["slug"] in G:
        u["gorseller"] = [{"d": a, "a": b} for a, b in G[u["slug"]]]

# Yilan: Playables bolumune
for u in d["urunler"]:
    if u["slug"] == "yilan":
        u["etiket"] = "TARAYICI OYUNU"
        u["kisa"] = "Klasik yılan oyunu. Kurulum gerektirmez, doğrudan tarayıcıda çalışır. YouTube Playables için de hazırlanacak."

json.dump(d, io.open(y, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("urunler.json guncellendi -", len(d["urunler"]), "urun")
for u in d["urunler"]:
    print("  %-14s gorsel:%d" % (u["slug"], len(u.get("gorseller", []))))
