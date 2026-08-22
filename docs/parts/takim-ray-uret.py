# -*- coding: utf-8 -*-
"""Dört büyük takım sayfasında sağ sütun rayına ÖNCEKİ/SONRAKİ düğmesi.

Talep (22 Ağustos akşamı): "Takım sayfalarında son maçlar fikstür kısmı
— sayfanın sağ tarafındaki — scrollbar'la sağa doğru götürülüyor. Buna
gerek yok. Önceki maç / sonraki maç mantığında gitsin, scrollbar
şeklinde gitmesin."

ÖLÇÜM: `.dh-mcrail` 371px kapta, içerik 884px — yatay kaydırma çubuğu
çıkıyordu. Ray zaten `data-dh-track` taşıyor ama `dh-track.js` düğmeleri
`data-dh-track-prev="<id>"` ile bağlıyor; rayın id'si yoktu, düğme de
yoktu. İkisi de burada eklenir.

Yeniden üret:  python3 docs/parts/takim-ray-uret.py
"""
import os, re, subprocess

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

SAYFALAR = ["takim-trabzonspor.html", "takim-fenerbahce.html",
            "takim-galatasaray.html", "takim-besiktas.html",
            "spor-takim-detay.html"]

NAV = ('<div class="dh-mcnav">'
       '<span class="dh-mcnav__n" data-dh-mcnav-sayac="%s" aria-live="polite"></span>'
       '<button type="button" class="dh-mcnav__b" data-dh-mcnav-prev="%s" '
       'aria-label="Önceki maç"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>'
       '<button type="button" class="dh-mcnav__b" data-dh-mcnav-next="%s" '
       'aria-label="Sonraki maç"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>'
       '</div>')

n = 0
for dosya in SAYFALAR:
    if not os.path.exists(dosya):
        continue
    s = open(dosya, encoding="utf-8").read()
    kok_ad = dosya.replace(".html", "").replace("-", "")
    sira = 0
    yeni = []
    son = 0
    for m in re.finditer(r'<div class="dh-mcrail"([^>]*)data-dh-track([^>]*)>', s):
        if 'id=' in m.group(0):
            continue
        sira += 1
        rid = "mcray-%s-%d" % (kok_ad, sira)
        yeni.append((m.start(), m.end(), rid, m.group(0)))
    if not yeni:
        print("  %s — eklenecek ray yok (id zaten var ya da ray yok)" % dosya)
        continue

    parca, son = [], 0
    for b, e, rid, ham in yeni:
        parca.append(s[son:b])
        # rayın id'si + hemen ÖNÜNE gezinme düğmeleri
        girinti = s[s.rfind("\n", 0, b) + 1:b]
        parca.append(NAV % (rid, rid, rid) + "\n" + girinti)
        # SINIF da ekleniyor: dh-track.js `document.querySelectorAll('.dh-track[id]')`
        # ile bağlanıyor — `data-dh-track` NİTELİĞİNE bakmıyor (ölçüldü: düğmeler
        # tıklanıyordu ama ray hiç kaymıyordu).
        parca.append(ham.replace('<div class="dh-mcrail"',
                                 '<div class="dh-mcrail" data-dh-mcnav id="%s"' % rid, 1))
        son = e
    parca.append(s[son:])
    s = "".join(parca)

    # bileşen betiği bağlı mı
    if "js/v2/dh-mcnav.js" not in s:
        m2 = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
        if m2:
            s = s[:m2.end()] + '    <script defer src="./assets/js/v2/dh-mcnav.js"></script>\n' + s[m2.end():]

    open(dosya, "w", encoding="utf-8").write(s)
    print("  %s — %d ray, önceki/sonraki düğmeleri eklendi" % (dosya, len(yeni)))
    n += 1

print("%d sayfa" % n)
