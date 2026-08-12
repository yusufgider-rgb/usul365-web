import io
y = "uret_site.py"
t = io.open(y, encoding="utf-8").read()
t = t.replace('bolum("tarayici", "Playables &mdash; Tarayıcıda", "Kurulum gerektirmeden doğrudan tarayıcıda çalışır; YouTube Playables için de hazırlanıyor.",',
              'bolum("playables", "Google Playables", "Tarayıcıda doğrudan oynanan sürümler; Google Playables için hazırlanıyor.",')
io.open(y, "w", encoding="utf-8").write(t)
print("bolum adi: Google Playables")
