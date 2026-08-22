# -*- coding: utf-8 -*-
"""sayfa-dizini.html — sitedeki bütün sayfaların adı ve adresi.

Talep: "Bütün sayfaları sayfa dizini diye bir html dosyasına yaz.
Karşılıklarına sayfa ismini ve karşılığında url yaz."

Liste ELLE TUTULMUYOR: kökteki *.html taranıyor, başlık <title>'dan
okunuyor. Yeni sayfa eklenince üreteci çalıştırmak yetiyor; unutulursa
denetim de yakalar (dizinde olmayan sayfa "sınıflanmamış" bölümüne düşer).

Yeniden üret:  python3 docs/parts/dizin-uret.py
"""
import glob, html, os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from sayfa_basligi import basli

SABLON = "docs/parts/sayfa-sablon.html"
HEDEF = "sayfa-dizini.html"
YAYIN = "https://gaviaworks-dev.github.io/dadahaber-view/v2/"

# Bölümler bilgi mimarisinden (docs/V2-IA.md) geliyor; ana menü sırasıyla.
BOLUM = [
 ("Anasayfa", "Sitenin giriş sayfası.", [
   ("index.html", "Anasayfa"),
 ]),
 ("Anlık", "Gelişmelerin dakikası dakikasına izlendiği bölüm.", [
   ("anlik.html", "Anlık Merkezi"),
   ("son-dakika.html", "Son Dakika"),
   ("canli-gundem.html", "Canlı Gündem"),
   ("dakika-dakika.html", "Dakika Dakika"),
   ("bugun-ne-oldu.html", "Bugün Ne Oldu?"),
   ("gundem-takvimi.html", "Gündem Takvimi"),
   ("guncellenen-haberler.html", "Güncellenen Haberler"),
   ("afet-acil-durum.html", "Afet ve Acil Durum"),
   ("trafik-ulasim.html", "Trafik ve Ulaşım"),
   ("hava-durumu.html", "Hava Durumu"),
 ]),
 ("Gündem", "Türkiye gündemi, yerel haberler ve özgün içerikler.", [
   ("gundem.html", "Gündem"),
   ("iller.html", "81 İl"),
 ]),
 ("Dünya", "Dış politika ve uluslararası gündem.", [
   ("dunya.html", "Dünya"),
   ("nato.html", "NATO"),
 ]),
 ("Finans", "Piyasa verileri, ekonomi haberleri ve araçlar.", [
   ("finans.html", "Finans"),
   ("ekonomi.html", "Ekonomi"),
   ("doviz.html", "Döviz Kurları"),
   ("altin.html", "Altın Fiyatları"),
   ("borsa.html", "Borsa ve Endeksler"),
   ("kripto.html", "Kripto Para"),
   ("faiz-oranlari.html", "Faiz Oranları"),
   ("ekonomik-takvim.html", "Ekonomik Takvim"),
 ]),
 ("Savunma", "Savunma sanayii ve güvenlik.", [
   ("savunma.html", "Savunma"),
 ]),
 ("Spor", "Tüm dallarda skor, puan durumu ve haber.", [
   ("spor.html", "Spor"),
   ("futbol.html", "Futbol"),
   ("basketbol.html", "Basketbol"),
   ("voleybol.html", "Voleybol"),
   ("formula1.html", "Formula 1"),
   ("bisiklet.html", "Bisiklet"),
   ("puan-durumu.html", "Puan Durumu"),
   ("fikstur.html", "Fikstür"),
   ("takim.html", "Takımlar"),
   ("takim-galatasaray.html", "Galatasaray"),
   ("takim-fenerbahce.html", "Fenerbahçe"),
   ("takim-besiktas.html", "Beşiktaş"),
   ("takim-trabzonspor.html", "Trabzonspor"),
 ]),
 ("Kadın", "Kadın gündemi, sağlık ve hamilelik rehberi.", [
   ("kadin.html", "Kadın"),
   ("hamilelik.html", "Hamilelik Rehberi"),
 ]),
 ("Diğer Kategoriler", "Ana menüden çıkan başlıklar; hepsi burada.", [
   ("diger.html", "Tüm Kategoriler Dizini"),
   ("teknoloji.html", "Teknoloji"),
   ("saglik.html", "Sağlık"),
   ("kultur-yasam.html", "Kültür & Yaşam"),
   ("gelecek.html", "Gelecek"),
   ("oyun.html", "Oyun"),
   ("astroloji.html", "Astroloji"),
   ("resmi-ilanlar.html", "Resmî İlanlar"),
 ]),
 ("Keşfet", "Dada Haber'in kendi üretim ve doğrulama araçları.", [
   ("kesfet.html", "Keşfet"),
   ("dada-ozet.html", "Dada Özet"),
   ("dada-baglam.html", "Dada Bağlam"),
   ("dada-dogrula.html", "Dada Doğrula"),
   ("farkli-bakislar.html", "Farklı Bakışlar"),
   ("veri-harita.html", "Veri & Harita"),
   ("sakin-akis.html", "Sakin Akış"),
 ]),
 ("Yayın Formatları", "Haberin metin dışındaki biçimleri.", [
   ("haber-dinle.html", "Haber Dinle"),
   ("foto-fokus.html", "Foto Fokus"),
   ("video.html", "Video Haber"),
   ("video-galeri.html", "Video Galeri"),
   ("infografik.html", "İnfografik"),
   ("podcast.html", "Podcast"),
 ]),
 ("Üyelik", "Hesap işlemleri.", [
   ("giris.html", "Giriş Yap"),
   ("uye-ol.html", "Üye Ol"),
   ("sifremi-unuttum.html", "Şifremi Unuttum"),
   ("hesabim.html", "Hesabım"),
 ]),
 ("Kurumsal", "Kurum bilgileri ve iletişim.", [
   ("hakkimizda.html", "Hakkımızda"),
   ("kunye.html", "Künye"),
   ("yayin-ilkeleri.html", "Yayın İlkeleri"),
   ("iletisim.html", "İletişim"),
   ("reklam.html", "Reklam"),
 ]),
 ("Yasal", "Kullanım koşulları ve veri metinleri.", [
   ("kullanim-sartlari.html", "Kullanım Koşulları"),
   ("kvkk.html", "Gizlilik ve KVKK"),
   ("aydinlatma-metni.html", "Aydınlatma Metni"),
   ("cerezler.html", "Çerez Politikası"),
 ]),
 ("Liste ve Yazar", "Arşiv, arama ve yazar sayfaları.", [
   ("haber-liste.html", "Haber Listesi"),
   ("arsiv.html", "Arşiv"),
   ("arama.html", "Arama Sonuçları"),
   ("yazar-liste.html", "Yazarlar"),
   ("yazar-detay.html", "Yazar Profili"),
   ("yazar-icerik-detay.html", "Yazar Yazısı"),
 ]),
 ("Detay Şablonları", "Her kategorinin haber detay kalıbı.", [
   ("haber-detay.html", "Haber Detay"),
   ("finans-detay.html", "Finans Detay"),
   ("savunma-detay.html", "Savunma Detay"),
   ("spor-detay.html", "Spor Detay"),
   ("spor-takim-detay.html", "Takım Detay"),
   ("kadin-detay.html", "Kadın Detay"),
   ("hamilelik-detay.html", "Hamilelik Detay"),
   ("saglik-detay.html", "Sağlık Detay"),
   ("teknoloji-detay.html", "Teknoloji Detay"),
   ("oyun-detay.html", "Oyun Detay"),
   ("video-detay.html", "Video Detay"),
   ("video-kategori-detay.html", "Video Kategori"),
   ("foto-fokus-detay.html", "Foto Galeri Detay"),
   ("foto-fokus-kategori-detay.html", "Foto Fokus Kategori"),
   ("podcast-detay.html", "Podcast Bölümü"),
   ("podcast-kategori-detay.html", "Podcast Kategori"),
   ("resmi-ilan-detay.html", "Resmî İlan Detayı"),
 ]),
 ("Sistem", "Yönlendirme ve hata sayfaları.", [
   ("404.html", "404 — Sayfa Bulunamadı"),
   ("coming-soon.html", "Çok Yakında"),
   ("simdi.html", "Şimdi (eski rota → Anlık)"),
   ("sayfa-dizini.html", "Sayfa Dizini (bu sayfa)"),
 ]),
]

# --- tarama: sınıflanmamış sayfa kaldı mı? ---------------------------------
mevcut = {os.path.basename(f) for f in glob.glob("*.html")}
listelenen = {d for _, _, ler in BOLUM for d, _ in ler}
eksik = sorted(mevcut - listelenen)
# İlk üretimde HEDEF henüz yok; kendisi eksik sayılmaz.
fazla = sorted(listelenen - mevcut - {HEDEF})
if fazla:
    sys.exit("HATA: dizinde olup dosyası olmayan sayfa: %s" % ", ".join(fazla))
if eksik:
    BOLUM.append(("Sınıflanmamış",
                  "Üreteçte bölümü yazılmamış sayfalar — dizin-uret.py'ye eklenmeli.",
                  [(d, d) for d in eksik]))

toplam = sum(len(l) for _, _, l in BOLUM)

g = []
w = g.append
w(basli("Kurumsal", "Sayfa Dizini",
        "Dada Haber prototipindeki bütün sayfalar; adı, adresi ve bulunduğu bölümle. "
        "Liste elle tutulmuyor, kökteki sayfalar taranarak üretiliyor.",
        [("Kurumsal", "hakkimizda.html"), ("Sayfa Dizini", None)], "img-16.jpg", "50% 46%",
        ["<b>%d</b> sayfa" % toplam, "<b>%d</b> bölüm" % len(BOLUM)]))

w('        <section class="section panel dh-dizin" id="dizin" aria-labelledby="dh-dizin-t">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n')
w('              <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-dizin-t">Bütün Sayfalar</h2>\n')
w('              <div class="dh-secbar__tools"><span class="dh-nwstamp">'
  '<i class="fas fa-sitemap" aria-hidden="true"></i> %d sayfa · %d bölüm</span></div>\n'
  % (toplam, len(BOLUM)))
w('            </div>\n')
w('            <p class="dh-nwintro">Her satırda sayfanın adı ve adresi var. Ada tıklayınca sayfa '
  'açılır. Adres sütunu yayındaki tam bağlantıyı gösterir.</p>\n')

for ad, aciklama, sayfalar in BOLUM:
    kimlik = re.sub(r"[^a-z0-9]+", "-", ad.lower().translate(
        str.maketrans("çğıöşüâ", "cgiosua"))).strip("-")
    w('\n            <section class="dh-dizin__grp" aria-labelledby="dz-%s">\n' % kimlik)
    w('              <header class="dh-dizin__hd">\n')
    w('                <h3 class="dh-dizin__h" id="dz-%s">%s</h3>\n' % (kimlik, html.escape(ad)))
    w('                <span class="dh-dizin__n">%d sayfa</span>\n' % len(sayfalar))
    w('              </header>\n')
    w('              <p class="dh-dizin__ac">%s</p>\n' % html.escape(aciklama))
    w('              <div class="dh-dizin__tablo" tabindex="0" role="region" aria-labelledby="dz-%s">\n' % kimlik)
    w('                <table class="dh-dizin__t">\n')
    w('                  <caption class="sr-only">%s bölümündeki sayfalar</caption>\n' % html.escape(ad))
    w('                  <thead><tr><th scope="col">Sayfa</th><th scope="col">Adres</th></tr></thead>\n')
    w('                  <tbody>\n')
    for dosya, sayfa_ad in sayfalar:
        w('                    <tr>\n')
        w('                      <th scope="row" class="dh-dizin__ad">'
          '<a href="%s">%s</a></th>\n' % (dosya, html.escape(sayfa_ad)))
        w('                      <td class="dh-dizin__url"><a href="%s">'
          '<span class="dh-dizin__kok">%s</span><b>%s</b></a></td>\n'
          % (dosya, YAYIN, dosya))
        w('                    </tr>\n')
    w('                  </tbody>\n')
    w('                </table>\n')
    w('              </div>\n')
    w('            </section>\n')

w('\n            <p class="dh-dizin__not"><i class="fas fa-circle-info" aria-hidden="true"></i> '
  'Bu liste <code>docs/parts/dizin-uret.py</code> ile üretilir; kökteki bütün <code>.html</code> '
  'dosyaları taranır. Yeni sayfa eklenip üreteç çalıştırılmazsa sayfa &ldquo;Sınıflanmamış&rdquo; '
  'başlığı altında görünür.</p>\n')
w('          </div>\n        </section>\n')
GOVDE = "".join(g)

s = open(SABLON, encoding="utf-8").read()
s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>", "<title>Sayfa Dizini — Dada Haber</title>")
if 'data-dh-cat=""' in s:
    s = s.replace('data-dh-cat=""', 'data-dh-cat="diger"', 1)
m = re.search(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", s, re.S)
if not m:
    sys.exit("HATA: gövde yuvası yok")
s = s[:m.start()] + GOVDE + s[m.end():]
open(HEDEF, "w", encoding="utf-8").write(s)
print("%s yazıldı — %d sayfa, %d bölüm%s"
      % (HEDEF, toplam, len(BOLUM), (" · SINIFLANMAMIŞ: %s" % ", ".join(eksik)) if eksik else ""))
