# -*- coding: utf-8 -*-
"""ekonomik-takvim.html ve faiz-oranlari.html — finans.html'deki iki panel
kendi sayfalarına çıktı ve veri genişletildi.

Panellerde sırasıyla 6 ve 8 satır vardı; sayfalarda 34 takvim kaydı ve
dört ayrı faiz tablosu var. Bileşenler mevcut: .dh-tkvm ve .dh-fintable.
Takvim süzgeci için tek küçük dosya yazıldı: assets/js/v2/dh-takvim.js
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from sayfa_basligi import basli
SABLON = "docs/parts/sayfa-sablon.html"

# ---------------------------------------------------------------- takvim
# (gün, saat, ülke, kod, olay, önceki, beklenti, önem)
TAKVIM = [
 ("BUGÜN","10.00","Türkiye","TR","Tüketici Güven Endeksi · Ağustos","84,1","85,0","yuksek"),
 ("BUGÜN","10.00","Türkiye","TR","Kapasite Kullanım Oranı · Ağustos","%76,3","%76,5","orta"),
 ("BUGÜN","11.00","Euro Bölgesi","EA","İmalat PMI · Öncü","49,8","50,1","yuksek"),
 ("BUGÜN","15.30","ABD","US","Haftalık İşsizlik Başvuruları","221 bin","218 bin","orta"),
 ("BUGÜN","17.00","ABD","US","İkinci El Konut Satışları","3,89 mn","3,95 mn","orta"),
 ("BUGÜN","21.00","ABD","US","FOMC Tutanakları","—","—","yuksek"),
 ("YARIN","09.00","Almanya","DE","GfK Tüketici Güveni · Eylül","-21,4","-20,8","orta"),
 ("YARIN","10.00","Türkiye","TR","Yurt Dışı Üretici Fiyat Endeksi","%1,8","%1,5","dusuk"),
 ("YARIN","11.30","İngiltere","GB","Perakende Satışlar · Temmuz","%0,3","%0,4","orta"),
 ("YARIN","15.30","ABD","US","Dayanıklı Mal Siparişleri","%-6,6","%1,2","yuksek"),
 ("YARIN","17.00","Euro Bölgesi","EA","Tüketici Güveni · Öncü","-13,0","-12,6","orta"),
 ("CMT","04.30","Japonya","JP","Tokyo TÜFE · Ağustos","%2,2","%2,3","orta"),
 ("CMT","09.00","Türkiye","TR","Turizm Geliri · İkinci Çeyrek","14,2 mlr $","15,1 mlr $","orta"),
 ("CMT","11.00","Almanya","DE","Ifo İş İklimi · Ağustos","87,0","86,6","yuksek"),
 ("PZR","04.30","Çin","CN","Sanayi Kârları · Temmuz","%3,6","%4,1","dusuk"),
 ("PZR","10.00","Türkiye","TR","Ekonomik Güven Endeksi · Ağustos","96,8","97,4","orta"),
 ("PZT","09.00","Türkiye","TR","Dış Ticaret Dengesi · Temmuz","-8,9 mlr $","-8,2 mlr $","yuksek"),
 ("PZT","11.00","Euro Bölgesi","EA","M3 Para Arzı · Temmuz","%2,3","%2,5","dusuk"),
 ("PZT","15.30","ABD","US","Kişisel Gelir · Temmuz","%0,2","%0,3","orta"),
 ("PZT","17.00","ABD","US","Tüketici Güveni · Ağustos","100,3","100,9","yuksek"),
 ("SAL","09.00","Türkiye","TR","İmalat Güven Endeksi · Ağustos","101,2","101,8","orta"),
 ("SAL","10.00","İngiltere","GB","Nationwide Konut Fiyatları","%0,3","%0,2","dusuk"),
 ("SAL","15.30","ABD","US","GSYH · İkinci Çeyrek Revize","%2,8","%3,0","yuksek"),
 ("SAL","16.45","ABD","US","Chicago PMI · Ağustos","47,4","48,0","orta"),
 ("ÇAR","04.30","Çin","CN","İmalat PMI · Ağustos","49,4","49,7","yuksek"),
 ("ÇAR","10.00","Türkiye","TR","TCMB Faiz Kararı","%32,50","%32,50","yuksek"),
 ("ÇAR","11.00","Euro Bölgesi","EA","TÜFE · Öncü · Ağustos","%2,6","%2,4","yuksek"),
 ("ÇAR","15.30","ABD","US","PCE Fiyat Endeksi · Temmuz","%2,5","%2,6","yuksek"),
 ("PER","09.00","Almanya","DE","Perakende Satışlar · Temmuz","%-0,6","%0,3","orta"),
 ("PER","10.00","Türkiye","TR","TÜFE · Ağustos","%1,64","%1,90","yuksek"),
 ("PER","11.00","İngiltere","GB","BoE Faiz Kararı","%4,75","%4,50","yuksek"),
 ("PER","15.30","ABD","US","Tarım Dışı İstihdam · Ağustos","114 bin","165 bin","yuksek"),
 ("PER","15.30","ABD","US","İşsizlik Oranı · Ağustos","%4,3","%4,2","yuksek"),
 ("PER","17.00","ABD","US","ISM İmalat · Ağustos","46,8","47,5","orta"),
]
ONEM_AD = {"yuksek": "Yüksek etki", "orta": "Orta etki", "dusuk": "Düşük etki"}
ULKELER = ["Türkiye", "ABD", "Euro Bölgesi", "Almanya", "İngiltere", "Japonya", "Çin"]

# ------------------------------------------------------------------ faiz
POLITIKA = [
 ("TCMB", "Türkiye · Politika faizi", "%32,50", "%35,00", "-2,50", "down", "27 Eylül 2026"),
 ("FED", "ABD · Federal fon oranı", "%4,75", "%5,00", "-0,25", "down", "18 Eylül 2026"),
 ("ECB", "Euro Bölgesi · Mevduat faizi", "%3,25", "%3,50", "-0,25", "down", "12 Eylül 2026"),
 ("BoE", "İngiltere · Banka faizi", "%4,75", "%5,00", "-0,25", "down", "19 Eylül 2026"),
 ("BoJ", "Japonya · Politika faizi", "%0,25", "%0,10", "+0,15", "up", "20 Eylül 2026"),
 ("SNB", "İsviçre · Politika faizi", "%1,00", "%1,25", "-0,25", "down", "26 Eylül 2026"),
 ("CBR", "Rusya · Anahtar faiz", "%18,00", "%16,00", "+2,00", "up", "13 Eylül 2026"),
 ("PBoC", "Çin · 1 yıllık LPR", "%3,35", "%3,45", "-0,10", "down", "20 Eylül 2026"),
]
MEVDUAT = [
 ("32 gün", "%41,50", "%42,25", "-0,75", "down"),
 ("46 gün", "%43,00", "%43,50", "-0,50", "down"),
 ("92 gün", "%44,25", "%44,00", "+0,25", "up"),
 ("181 gün", "%42,75", "%43,10", "-0,35", "down"),
 ("365 gün", "%39,50", "%40,00", "-0,50", "down"),
 ("Katılım · 32 gün", "%38,80", "%39,10", "-0,30", "down"),
]
KREDI = [
 ("İhtiyaç kredisi", "%4,29", "%4,35", "-0,06", "down"),
 ("Taşıt kredisi", "%3,89", "%3,89", "0,00", ""),
 ("Konut kredisi", "%2,79", "%2,84", "-0,05", "down"),
 ("Ticari kredi", "%4,05", "%4,12", "-0,07", "down"),
 ("Kredi kartı akdi", "%4,25", "%4,25", "0,00", ""),
 ("KMH · gecikme", "%5,15", "%5,15", "0,00", ""),
]
SEYIR = [
 ("Ağustos 2026", "%32,50", "-2,50"), ("Haziran 2026", "%35,00", "-2,50"),
 ("Nisan 2026", "%37,50", "-2,50"), ("Şubat 2026", "%40,00", "-2,50"),
 ("Aralık 2025", "%42,50", "-5,00"), ("Ekim 2025", "%47,50", "-2,50"),
 ("Ağustos 2025", "%50,00", "0,00"),
]


def tablo(baslik, altyazi, basliklar, satirlar, tid):
    o = []
    o.append('            <section class="dh-finpanel" id="%s" data-cat="finans" aria-labelledby="%s-b">\n' % (tid, tid))
    o.append('              <div class="dh-finpanel__head"><div>\n')
    o.append('                <h2 class="dh-finpanel__title" id="%s-b">%s</h2>\n' % (tid, baslik))
    o.append('                <span class="dh-finpanel__sub">%s</span>\n' % altyazi)
    o.append('              </div></div>\n')
    o.append('              <div class="dh-finpanel__body"><div class="dh-fintable__scroll">\n')
    o.append('                <table class="dh-fintable"><caption class="sr-only">%s</caption>\n' % baslik)
    o.append('                  <thead><tr>')
    for i, b in enumerate(basliklar):
        o.append('<th scope="col"%s>%s</th>' % ('' if i == 0 else ' class="is-num"', b))
    o.append('</tr></thead>\n                  <tbody>\n')
    for sat in satirlar:
        o.append(sat)
    o.append('                  </tbody>\n                </table>\n')
    o.append('              </div></div>\n            </section>\n')
    return "".join(o)


def govde_takvim():
    o = []; w = o.append
    yuksek = sum(1 for t in TAKVIM if t[7] == "yuksek")
    w(basli("Finans", "Ekonomik Takvim",
            "Önümüzdeki yedi günde açıklanacak veriler, saatleri ve piyasa beklentileri. "
            "Saatler Türkiye saatidir.",
            [("Finans", "ekonomi.html"), ("Ekonomik Takvim", None)], "img-13.jpg", "50% 46%",
            ["<b>%d</b> veri" % len(TAKVIM), "<b>%d</b> yüksek etkili" % yuksek]))
    w('        <section class="section panel"><div class="container max-w-xl">\n')
    w('          <div class="section-header panel dh-secbar">\n')
    w('            <h2 class="h5 xl:h4 m-0 text-black dark:text-white">Bu Hafta</h2>\n')
    w('            <div class="dh-secbar__tools"><span class="dh-nwstamp">'
      '<i class="fas fa-calendar-day" aria-hidden="true"></i> %d veri · <b>%d</b> yüksek etkili</span></div>\n'
      % (len(TAKVIM), yuksek))
    w('          </div>\n')
    # süzgeçler
    w('          <div class="dh-tkfilt" data-dh-takvim>\n')
    w('            <div class="dh-tkfilt__grp" role="radiogroup" aria-label="Ülke süzgeci">\n')
    w('              <span class="dh-tkfilt__lbl">Ülke</span>\n')
    w('              <button type="button" class="dh-tkfilt__b is-on" role="radio" aria-checked="true" data-dh-tk-ulke="">Tümü</button>\n')
    for u in ULKELER:
        w('              <button type="button" class="dh-tkfilt__b" role="radio" aria-checked="false" data-dh-tk-ulke="%s">%s</button>\n' % (u, u))
    w('            </div>\n')
    w('            <div class="dh-tkfilt__grp" role="radiogroup" aria-label="Etki süzgeci">\n')
    w('              <span class="dh-tkfilt__lbl">Etki</span>\n')
    w('              <button type="button" class="dh-tkfilt__b is-on" role="radio" aria-checked="true" data-dh-tk-onem="">Tümü</button>\n')
    for k, ad in (("yuksek", "Yüksek"), ("orta", "Orta"), ("dusuk", "Düşük")):
        w('              <button type="button" class="dh-tkfilt__b" role="radio" aria-checked="false" data-dh-tk-onem="%s">%s</button>\n' % (k, ad))
    w('            </div>\n')
    w('            <p class="dh-tkfilt__say" role="status"><b data-dh-tk-say>%d</b> kayıt gösteriliyor</p>\n' % len(TAKVIM))
    w('          </div>\n')
    w('          <ol class="dh-tkvm dh-tkvm--sayfa" data-dh-tk-liste>\n')
    for i, (gun, saat, ulke, kod, olay, onc, bek, onem) in enumerate(TAKVIM):
        simdi = ' is-now' if i == 0 else ''
        w('            <li class="dh-tkvm__it%s" data-onem="%s" data-ulke="%s">\n' % (simdi, onem, ulke))
        w('              <span class="dh-tkvm__when dh-num"><b>%s</b>%s</span>\n' % (gun, saat))
        w('              <span class="dh-tkvm__what">\n')
        w('                <span class="dh-tkvm__ulke">%s</span>\n' % ulke)
        w('                <span class="dh-tkvm__ad">%s</span>\n' % olay)
        w('                <span class="dh-tkvm__nums dh-num">ÖNCEKİ %s · BEKLENTİ %s</span>\n' % (onc, bek))
        w('              </span>\n')
        w('              <span class="dh-tkvm__onem">%s</span>\n' % ONEM_AD[onem])
        w('            </li>\n')
    w('          </ol>\n')
    w('          <p class="dh-nato__not"><i class="fas fa-circle-info" aria-hidden="true"></i> '
      'Takvimdeki tarih, saat ve beklenti değerleri prototip için üretilmiş yer tutuculardır.</p>\n')
    w('        </div></section>\n')
    return "".join(o)


def govde_faiz():
    o = []; w = o.append
    def sat(ad, aciklama, *hucre, dir=""):
        d = ' data-dir="%s"' % dir if dir else ''
        h = "".join('<td class="is-num">%s</td>' % x for x in hucre)
        ac = '<span class="dh-fintable__desc">%s</span>' % aciklama if aciklama else ''
        return ('                    <tr%s><th scope="row" class="dh-fintable__name">'
                '<span class="dh-fintable__code">%s</span>%s</th>%s</tr>\n' % (d, ad, ac, h))

    w(basli("Finans", "Faiz Oranları",
            "Merkez bankası politika faizleri, mevduat ve kredi oranları bir arada. "
            "Oranlar yıllıktır; bankalar arası ortalamayı gösterir.",
            [("Finans", "ekonomi.html"), ("Faiz Oranları", None)], "img-09.jpg", "50% 50%",
            ["<b>4</b> tablo", "<b>8</b> merkez bankası"]))
    w('        <section class="section panel"><div class="container max-w-xl">\n')
    w('          <div class="dh-fingrid dh-fingrid--sayfa">\n')

    w(tablo("Merkez Bankası Politika Faizleri",
            "Sekiz merkez bankası · son karar ve bir sonraki toplantı",
            ["Banka", "Güncel", "Önceki", "Değişim", "Sonraki toplantı"],
            [sat(k, a, g, o2, d, t, dir=y) for k, a, g, o2, d, y, t in POLITIKA],
            "politika"))
    w(tablo("Mevduat Faizleri", "Vadeye göre · bankalar arası ortalama · 20 Ağustos 2026",
            ["Vade", "Oran", "Önceki", "Değişim"],
            [sat(v, "", o2, on, d, dir=y) for v, o2, on, d, y in MEVDUAT],
            "mevduat"))
    w(tablo("Kredi Faizleri", "Aylık oran · bankalar arası ortalama",
            ["Kalem", "Oran", "Önceki", "Değişim"],
            [sat(k, "", o2, on, d, dir=y) for k, o2, on, d, y in KREDI],
            "kredi"))
    w(tablo("TCMB Politika Faizi Seyri", "Son yedi karar",
            ["Toplantı", "Faiz", "Değişim"],
            [sat(t, "", f, d) for t, f, d in SEYIR],
            "seyir"))

    w('          </div>\n')
    w('          <p class="dh-nato__not"><i class="fas fa-circle-info" aria-hidden="true"></i> '
      'Oranlar prototip için üretilmiş yer tutuculardır; yatırım tavsiyesi değildir. '
      '<a href="finans.html">Piyasa ekranı</a> · <a href="ekonomik-takvim.html">Ekonomik takvim</a></p>\n')
    w('        </div></section>\n')
    return "".join(o)


SABLON_S = open(SABLON, encoding="utf-8").read()
yuva = re.compile(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", re.S)

for dosya, baslik, govde, betik in (
    ("ekonomik-takvim.html", "Ekonomik Takvim", govde_takvim(), "dh-takvim.js"),
    ("faiz-oranlari.html", "Faiz Oranları", govde_faiz(), None),
):
    s = SABLON_S
    s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>", "<title>%s — Dada Haber</title>" % baslik)
    if 'data-dh-cat=""' in s:
        s = s.replace('data-dh-cat=""', 'data-dh-cat="ekonomi"', 1)
    m = yuva.search(s)
    if not m:
        sys.exit("HATA: gövde yuvası yok")
    s = s[:m.start()] + govde + s[m.end():]
    if betik:
        m2 = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
        s = s[:m2.end()] + '    <script defer src="./assets/js/v2/%s"></script>\n' % betik + s[m2.end():]
    open(dosya, "w", encoding="utf-8").write(s)
    print("%s yazıldı (%d satır)" % (dosya, len(s.splitlines())))
