import json, io
d = json.load(io.open(r'icerik\urunler.json', encoding='utf-8'))
for u in d['urunler']:
    if u['slug'] == 'blok-dusur':
        u['fiyat'] = '250 TL'
        u['etiket'] = 'OYUN'
        u['kisa'] = 'Klasik blok yerleştirme oyunu. On dilde arayüz, üç zorluk seviyesi ve kalıcı istatistikler. Windows sürümü Microsoft Store''da; tarayıcı sürümü ücretsiz oynanabilir.'
    if u['slug'] == 'yilan':
        u['etiket'] = 'TARAYICI OYUNU · ÜCRETSİZ'
json.dump(d, io.open(r'icerik\urunler.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('Blok fiyat: 250 TL')
