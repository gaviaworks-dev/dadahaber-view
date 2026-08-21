# -*- coding: utf-8 -*-
"""v2 kabuğunu tüm kök HTML sayfalarına yayar. Idempotent — tekrar çalıştırılabilir."""
import glob, os, re, sys

d = os.path.dirname(os.path.abspath(__file__))
HDR = open(os.path.join(d, "header.html"), encoding="utf-8").read()
OFF = open(os.path.join(d, "offcanvas.html"), encoding="utf-8").read()
FTR = open(os.path.join(d, "footer.html"), encoding="utf-8").read()

CSS_LINK = '  <link rel="stylesheet" href="./assets/css/theme/v2.css">\n'

def kapat_div(s, i):
    """i: '<div' başlangıç indisi. Dengeli </div> sonrası indisi döndürür."""
    n, j = 0, i
    for m in re.finditer(r"<div\b|</div>", s[i:]):
        if m.group(0) == "<div":
            n += 1
        else:
            n -= 1
            if n == 0:
                return i + m.end()
    return -1

def satir_basi(s, i):
    j = s.rfind("\n", 0, i)
    return j + 1 if j != -1 else 0

def isle(yol):
    s = open(yol, encoding="utf-8").read()
    orj = s
    rapor = []

    # 1) offcanvas
    i = s.find('<div id="uc-menu-panel"')
    if i != -1:
        b = satir_basi(s, i)
        e = kapat_div(s, i)
        if e == -1:
            return None, "offcanvas kapanmıyor"
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        s = s[:b] + OFF + s[e:]
        rapor.append("menu")

    # 2) header
    m = re.search(r"[ \t]*<!-- Header start -->", s)
    if m:
        b = m.start()
        k = s.find("</header>", m.end())
        if k == -1:
            return None, "header kapanmıyor"
        e = k + len("</header>")
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        s = s[:b] + HDR + s[e:]
        rapor.append("header")

    # 3) footer
    i = s.find('<footer id="uc-footer"')
    if i != -1:
        b = satir_basi(s, i)
        k = s.find("</footer>", i)
        if k == -1:
            return None, "footer kapanmıyor"
        e = k + len("</footer>")
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        s = s[:b] + FTR + s[e:]
        rapor.append("footer")

    # 4) v2.css bağlantısı
    if "theme/v2.css" not in s:
        m = re.search(r'[ \t]*<link rel="stylesheet" href="\./assets/css/theme/custom\.min\.css">[ \t]*\n', s)
        if m:
            s = s[:m.end()] + CSS_LINK + s[m.end():]
            rapor.append("css")
        else:
            return None, "custom.min.css bağlantısı yok"

    # 4b) aktif menü betiği
    if "js/v2/dh-v2-nav.js" not in s:
        m = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
        if m:
            s = s[:m.end()] + '    <script defer src="./assets/js/v2/dh-v2-nav.js"></script>\n' + s[m.end():]
            rapor.append("navjs")

    # 5) yapışkan kenar sütunu ofseti: 136 → 120 (yeni kabuk yapışkanda 104px)
    if "offset: 136" in s:
        s = s.replace("offset: 136", "offset: 120")
        rapor.append("offset")

    if s != orj:
        open(yol, "w", encoding="utf-8").write(s)
    return rapor, None

ok, atla = 0, []
for yol in sorted(glob.glob("*.html")):
    r, hata = isle(yol)
    if hata:
        atla.append((yol, hata))
    else:
        ok += 1
        eksik = [x for x in ("menu", "header", "footer") if x not in r]
        if eksik:
            atla.append((yol, "eksik: " + ",".join(eksik)))
print("işlenen: %d" % ok)
for y, h in atla:
    print("  ! %s — %s" % (y, h))
