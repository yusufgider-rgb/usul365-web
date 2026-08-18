/* USUL365 ortak kabuk. Tek degisiklik noktasi: asagidaki MENU ve ALT dizileri. */
(function(){
  var MENU = [
    ["Yol Haritası", "/yol-haritasi.html"],
    ["Kurumsal",    "/kurumsal.html"],
    ["Destek",      "mailto:destek@usul365.com"]
  ];
  var ALT = [
    ["Ürünler", [
      ["Guard",       "/uygulamalar/guard/"],
      ["Namaz Vakti", "/uygulamalar/namaz-vakti/"],
      ["HesapPro",    "/#uygulamalar"],
      ["Blok Düşür",  "/oyunlar/blok-dusur/"]
    ]],
    ["Kurumsal", [
      ["Hakkımızda",         "/kurumsal.html"],
      ["Yol Haritası",        "/yol-haritasi.html"],
      ["destek@usul365.com", "mailto:destek@usul365.com"],
      ["Gizlilik Politikası","/gizlilik.html"],
      ["YouTube",            "https://www.youtube.com/@usul365"],
      ["X",                  "https://x.com/usul365"]
    ]]
  ];
  var SLOGAN = "Windows için sade, çevrimdışı çalışan masaüstü uygulamaları.";
  var TELIF  = "&copy; 2026 USUL365 — Yusuf Gider. Tüm hakları saklıdır.";
  var yol = location.pathname;

  var m = MENU.map(function(x){
    var etkin = (x[1] !== "/" && x[1].indexOf("#") < 0 && yol.indexOf(x[1]) === 0) ? " class=\"u-etkin\"" : "";
    return '<a href="' + x[1] + '"' + etkin + '>' + x[0] + '</a>';
  }).join("");

  var bar = document.createElement("div");
  bar.id = "u-bar";
  bar.innerHTML = '<div class="u-en"><a class="u-marka" href="/">' +
    '<img src="/gorseller/usul365_menu.png" alt="">USUL365</a><nav>' + m + '</nav></div>';
  document.body.insertBefore(bar, document.body.firstChild);

  var sut = ALT.map(function(g){
    return '<div><div class="u-fbaslik">' + g[0] + '</div>' +
      g[1].map(function(x){ return '<a href="' + x[1] + '">' + x[0] + '</a>'; }).join("") + '</div>';
  }).join("");

  var alt = document.createElement("footer");
  alt.id = "u-alt";
  alt.innerHTML = '<div class="u-en"><div class="u-izgara">' +
    '<div><div class="u-fmarka">USUL365</div><div class="u-fslogan">' + SLOGAN + '</div></div>' +
    sut + '</div><div class="u-falt"><div>' + TELIF + '</div><div id="u-sayac"></div></div></div>';
  document.body.appendChild(alt);
})();


/* ==== USUL365_SAYIM - gorunmez ziyaret sayimi ====
   Hicbir sey gostermez. Sadece sayar. Rakami sahibi API'den okur. */
(function () {
  var API = 'https://countapi.mileshilliard.com/api/v1/hit/';

  try {
    if (new URLSearchParams(location.search).get('ben') === '1') {
      localStorage.setItem('usul365_sahip', '1');
    }
  } catch (e) {}

  function sahip() {
    try { return localStorage.getItem('usul365_sahip') === '1'; }
    catch (e) { return false; }
  }

  function say(anahtar) {
    if (!anahtar || sahip()) return;
    try { new Image().src = API + anahtar + '?t=' + Date.now(); } catch (e) {}
  }

  var y = location.pathname.replace(/index\.html$/, '');
  var SAYFA = {
    '/': 'usul365_com_visits',
    '/kurumsal.html': 'usul365_sayfa_kurumsal',
    '/yol-haritasi.html': 'usul365_sayfa_yolharitasi',
    '/guncellemeler.html': 'usul365_sayfa_guncellemeler',
    '/gizlilik.html': 'usul365_sayfa_gizlilik',
    '/uygulamalar/guard/': 'usul365_sayfa_guard',
    '/uygulamalar/hesappro/': 'usul365_sayfa_hesappro',
    '/uygulamalar/namaz-vakti/': 'usul365_sayfa_namazvakti',
    '/uygulamalar/blok-dusur/': 'usul365_sayfa_blok'
  };
  say(SAYFA[y] || (y.indexOf('/kanallar/') === 0 ?
    'usul365_kanal_' + y.split('/')[2].replace('.html','').replace(/-/g,'') : null));

  var URUN = {
    '9pf0xqkv3dft': 'usul365_click_guard',
    '9p9rf8sd20sj': 'usul365_click_hesappro',
    '9n14sf0jmd4j': 'usul365_click_blok_store',
    '9mwcjzhf6l2w': 'usul365_click_namaz'
  };
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var h = (a.getAttribute('href') || '').toLowerCase();
    if (h.indexOf('apps.microsoft.com') === -1) return;
    for (var id in URUN) { if (h.indexOf(id) !== -1) { say(URUN[id]); return; } }
  }, true);
})();
