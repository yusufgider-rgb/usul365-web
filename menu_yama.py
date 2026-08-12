import io
y = "ortak.js"
t = io.open(y, encoding="utf-8").read()
t = t.replace('["Oyunlar",     "/#oyunlar"],',
              '["Oyunlar",     "/#oyunlar"],\n    ["Playables",   "/#playables"],')
io.open(y, "w", encoding="utf-8").write(t)
print("menuye Playables eklendi")
