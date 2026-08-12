/* USUL365 ortak kabuk. Tek degisiklik noktasi: asagidaki MENU ve ALT dizileri. */
(function(){
  var MENU = [
    ["Uygulamalar", "/#uygulamalar"],
    ["Oyunlar",     "/#oyunlar"],
    ["Playables",   "/#playables"],
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
    '<img src="/usul365_logo.jpeg" alt="">USUL365</a><nav>' + m + '</nav></div>';
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
