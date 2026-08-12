import io
y = "uret_site.py"
t = io.open(y, encoding="utf-8").read()

t = t.replace(
 '''    gor = "".join('<figure><img src="gorseller/%s" alt="%s"></figure>' % (g, e(u["ad"])) for g in gorseller(u["slug"]))''',
 '''    _ac = {x["d"]: x["a"] for x in u.get("gorseller", [])}
    gor = "".join('<figure><img src="gorseller/%s" alt="%s"><figcaption>%s</figcaption></figure>'
                  % (g, e(u["ad"]), e(_ac.get(g, ""))) for g in gorseller(u["slug"]))''')

t = t.replace(
 '''    bolum("tarayici", "Oyunlar &mdash; Tarayıcıda", "Kurulum gerektirmeden doğrudan tarayıcıda çalışır.",''',
 '''    bolum("tarayici", "Playables &mdash; Tarayıcıda", "Kurulum gerektirmeden doğrudan tarayıcıda çalışır; YouTube Playables için de hazırlanıyor.",''')

io.open(y, "w", encoding="utf-8").write(t)
print("uret_site.py guncellendi")
