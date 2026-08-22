# -*- coding: utf-8 -*-
"""v2 kabuğunu tüm kök HTML sayfalarına yayar. Idempotent — tekrar çalıştırılabilir."""
import glob, os, re, sys

d = os.path.dirname(os.path.abspath(__file__))
HDR = open(os.path.join(d, "header.html"), encoding="utf-8").read()
OFF = open(os.path.join(d, "offcanvas.html"), encoding="utf-8").read()
FTR = open(os.path.join(d, "footer.html"), encoding="utf-8").read()
BNV = open(os.path.join(d, "bnav.html"), encoding="utf-8").read()
CEREZ = open(os.path.join(d, "cerez.html"), encoding="utf-8").read()
BILDIRIM = open(os.path.join(d, "bildirim.html"), encoding="utf-8").read()

YUZEN = """  <!-- Sağ alt yüzen yığın: yukarı çık + karanlık mod -->
  <div class="backtotop-wrap position-fixed bottom-0 end-0 z-99 m-2 vstack">
    <a class="btn btn-sm bg-primary text-white w-40px h-40px rounded" href="#" data-uc-backtotop aria-label="Yukarı çık">
      <i class="icon-2 unicon-chevron-up"></i>
    </a>
    <div class="darkmode-trigger dh-v2-tema" data-darkmode-switch>
      <label class="switch dh-v2-tema__btn"><span class="sr-only">Karanlık mod</span><input type="checkbox"><span class="slider" aria-hidden="true"></span></label>
    </div>
  </div>
"""

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

    # Yönlendirme/uyumluluk sayfalarında kabuk yok — atlanır.
    if 'http-equiv="refresh"' in s:
        return ["atlandi"], None

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

    # 4b2) footer perdesi betiği (V1 deseni)
    if "js/footer-reveal.js" not in s:
        m = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
        if m:
            s = s[:m.end()] + '    <script defer src="./assets/js/footer-reveal.js"></script>\n' + s[m.end():]
            rapor.append("perde")

    # 4c) perdeleme menü + kullanıcı menüsü betiği
    if "js/v2/dh-v2-menu.js" not in s:
        m = re.search(r'[ \t]*<script defer src="\./assets/js/v2/dh-v2-nav\.js"></script>[ \t]*\n', s)
        if m:
            s = s[:m.end()] + '    <script defer src="./assets/js/v2/dh-v2-menu.js"></script>\n' + s[m.end():]
            rapor.append("menujs")

    # 5) yapışkan kenar sütunu ofseti: 136 → 120 (yeni kabuk yapışkanda 104px)
    if "offset: 136" in s:
        s = s.replace("offset: 136", "offset: 120")
        rapor.append("offset")

    # 6) sağ alt yüzen yığın: YUKARI ÇIK üstte, KARANLIK MOD onun altında.
    #    Tek kaynaktan kurulur ki 87 sayfada sıra aynı olsun.
    i = s.find('<div class="backtotop-wrap')
    if i != -1:
        b = satir_basi(s, i)
        e = kapat_div(s, i)
        if e == -1:
            return None, "backtotop-wrap kapanmıyor"
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        if s[b:e] != YUZEN:
            s = s[:b] + YUZEN + s[e:]
            rapor.append("yuzen")

    # 7) mobil alt gezinme çubuğu — tek kaynaktan yayılır
    m = re.search(r'[ \t]*<!--[^\n]*[Mm]obil alt gezinme[^\n]*-->\n', s)
    i = s.find('<nav class="dh-bnav"')
    if i != -1:
        b = m.start() if (m and m.end() <= i) else satir_basi(s, i)
        k = s.find("</nav>", i)
        if k == -1:
            return None, "dh-bnav kapanmıyor"
        e = k + len("</nav>")
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        s = s[:b] + BNV + s[e:]
        rapor.append("bnav")

    # 8) çerez rıza bandı + Gizlilik Tercih Merkezi — tek kaynak
    #    SINIF ADI: .dh-cz. `.dh-riza` KULLANILAMAZ — cerezler.html'de
    #    aynı adla eski bir bileşen var; ilk sürüm onu yay.py ile ezdi.
    #    Vendor bandı (#uc-gdpr-notification) DOM'da KALIR: app-head-bs.js ona
    #    koşulsuz addEventListener bağlıyor ve o dosya v1 ile paylaşılıyor.
    #    Görsel olarak j-riza.css kapatıyor.
    i = s.find('<div class="dh-cz"')
    if i != -1:
        b = satir_basi(s, i)
        e = kapat_div(s, i)
        if e == -1:
            return None, "dh-cz kapanmıyor"
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        if s[b:e] != CEREZ:
            s = s[:b] + CEREZ + s[e:]
            rapor.append("cerez")
    else:
        k = s.rfind("</body>")
        if k != -1:
            b = satir_basi(s, k)
            s = s[:b] + CEREZ + s[b:]
            rapor.append("cerez")

    # 8a2) bildirim izni kartı — çerez bandının hemen ardından
    i = s.find('<div class="dh-bld"')
    if i != -1:
        b = satir_basi(s, i)
        e = kapat_div(s, i)
        if e == -1:
            return None, "dh-bld kapanmıyor"
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        if s[b:e] != BILDIRIM:
            s = s[:b] + BILDIRIM + s[e:]
            rapor.append("bildirim")
    else:
        j = s.find('<div class="dh-cz"')
        if j != -1:
            k2 = kapat_div(s, j)
            if k2 != -1:
                while k2 < len(s) and s[k2] in " \t":
                    k2 += 1
                if k2 < len(s) and s[k2] == "\n":
                    k2 += 1
                s = s[:k2] + BILDIRIM + s[k2:]
                rapor.append("bildirim")

    # 8a3) bülten açılır penceresi kaldırılır (talep: "bu kısım kalkacak")
    #      Vendor app-head-bs.js 10 saniye sonra açıyordu; işaretleme
    #      buradan siliniyor, bayrağı da dh-bulten.js yazıyor.
    i = s.find('<div id="uc-newsletter-modal"')
    if i != -1:
        b = satir_basi(s, i)
        e = kapat_div(s, i)
        if e == -1:
            return None, "uc-newsletter-modal kapanmıyor"
        while e < len(s) and s[e] in " \t":
            e += 1
        if e < len(s) and s[e] == "\n":
            e += 1
        s = s[:b] + s[e:]
        rapor.append("bulten")

    if "js/v2/dh-bulten.js" not in s:
        m = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
        if m:
            s = s[:m.end()] + '    <script defer src="./assets/js/v2/dh-bulten.js"></script>\n' + s[m.end():]
            rapor.append("bultenjs")

    # 8b) rıza betiği
    if "js/v2/dh-cerez.js" not in s:
        m = re.search(r'[ \t]*<script defer src="\./assets/js/v2/dh-v2-menu\.js"></script>[ \t]*\n', s)
        if m:
            s = s[:m.end()] + '    <script defer src="./assets/js/v2/dh-cerez.js"></script>\n' + s[m.end():]
            rapor.append("cerezjs")

    if "js/v2/dh-bildirim.js" not in s:
        m = re.search(r'[ \t]*<script defer src="\./assets/js/v2/dh-cerez\.js"></script>[ \t]*\n', s)
        if m:
            s = s[:m.end()] + '    <script defer src="./assets/js/v2/dh-bildirim.js"></script>\n' + s[m.end():]
            rapor.append("bildirimjs")

    if s != orj:
        open(yol, "w", encoding="utf-8").write(s)
    return rapor, None

def tumu():
    ok, atla = 0, []
    for yol in sorted(glob.glob("*.html")):
        r, hata = isle(yol)
        if hata:
            atla.append((yol, hata))
        else:
            ok += 1
            eksik = [] if "atlandi" in r else [x for x in ("menu", "header", "footer") if x not in r]
            if eksik:
                atla.append((yol, "eksik: " + ",".join(eksik)))
    print("işlenen: %d" % ok)
    for y, h in atla:
        print("  ! %s — %s" % (y, h))


# Betik doğrudan çalıştırıldığında tüm sayfalara yayar. İçe aktarıldığında
# yalnız isle() kullanılabilir olsun diye ayrıldı: anlik-uret.py yeni ürettiği
# sayfalara kabuğu tek tek koyuyor, site geneline dokunmuyor.
if __name__ == "__main__":
    tumu()
