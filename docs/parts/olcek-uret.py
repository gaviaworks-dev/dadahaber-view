# -*- coding: utf-8 -*-
"""TİPOGRAFİ ÖLÇEĞİ — donmuş custom.min.css için override üreteci.

custom.min.css DEĞİŞTİRİLEMEZ (/v1/ arşivi aynı dosyayı paylaşıyor:
v1-kopya.py yalnız HTML kopyalayıp yolları ../assets/'e çeviriyor).
Bu yüzden merdiven dışı her font-size bildirimi için v2 tarafında
AYNI SEÇİCİYLE ve AYNI ortam sorgusu içinde bir override üretilir.

Sıralama: çıktı v2.css'in İLK parçasıdır. Böylece
  custom.min.css  <  z-olcek.css  <  v2'nin kendi parçaları
custom.min.css'i yener, v2'nin bilinçli kararlarını yenmez.

Kapsam dışı bırakılanlar (bilerek):
  · ikon/glif boyutları — metin rolü değil, merdiven anlamsız
  · 40px üstü — filigran/dekoratif ölçüler (ör. .dh-ph__stamp 92px)

Yeniden üret:  python3 docs/parts/olcek-uret.py
"""
import os, re, subprocess, glob, collections

MERDIVEN = [11, 12.5, 14, 16, 18, 22, 26, 30, 36]
TAVAN = 48                      # üstü dekoratif sayılır, dokunulmaz
                                # (440px .dh-mark filigranı, 148px 404 kodu, 92px .dh-ph__stamp)
KAYNAK = "assets/css/theme/custom.min.css"
HEDEF = "assets/css/theme/v2/z-olcek.css"

# metin değil ikon/glif olduğu seçiciden belli olanlar
IKON = re.compile(
    r"(?:^|[\s>+~])i(?:[.:\[]|$)"          # <i> öğesi
    r"|\bicon\b|\bicons?-|uil-|\bfa-|\bui-"
    r"|arrow|chevron|caret|glyph|dot\b|bullet"
    r"|close-btn|play-pause|\bplay\b|pause"
    r"|::(?:before|after)"
    r"|swiper-button|slider-nav|nav-(?:prev|next)",
    re.I)

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)


def kademe(v):
    return min(MERDIVEN, key=lambda s: (abs(s - v), -s))


def px_yaz(v):
    return ("%g" % v) + "px"


def uzunluk(tok):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)px", tok)
    if m:
        return float(m.group(1))
    m = re.fullmatch(r"(\d+(?:\.\d+)?)rem", tok)
    if m:
        return float(m.group(1)) * 16
    return None


def deger_cevir(ham):
    """font-size değerini merdivene oturt. Değişmiyorsa/kapsam dışıysa None."""
    ham = ham.strip()
    onemli = "!important" in ham
    gov = ham.replace("!important", "").strip()
    son = " !important" if onemli else ""

    tek = uzunluk(gov)
    if tek is not None:
        if tek > TAVAN:
            return None
        y = kademe(tek)
        return None if abs(y - tek) < 0.001 else px_yaz(y) + son

    if gov.startswith("clamp(") and gov.endswith(")"):
        parts = [p.strip() for p in gov[6:-1].split(",")]
        if len(parts) != 3:
            return None
        yeni, degisti = [], False
        for idx, p in enumerate(parts):
            v = uzunluk(p)
            if v is None or idx == 1 or v > TAVAN:   # orta terim akışkan
                yeni.append(p)
                continue
            y = kademe(v)
            if abs(y - v) >= 0.001:
                degisti = True
            yeni.append(px_yaz(y))
        return ("clamp(%s)" % ", ".join(yeni) + son) if degisti else None
    return None


def ayristir(css):
    """(ortam_sorgulari, secici, bildirimler) üretir. Süslü parantez yığını."""
    yigin, sonuc = [], []
    son, i, n = 0, 0, len(css)
    while i < n:
        c = css[i]
        if c == "{":
            yigin.append((css[son:i].strip(), i + 1))
            son = i + 1
        elif c == "}":
            if yigin:
                basi, govde_bas = yigin.pop()
                if basi and not basi.startswith("@"):
                    ortam = [b for b, _ in yigin if b.startswith("@")]
                    sonuc.append((ortam, basi, css[govde_bas:i]))
            son = i + 1
        i += 1
    return sonuc


# --- v2'nin kendi seçicileri: bunlara dokunma -------------------------------
v2_secici = set()
for f in glob.glob("assets/css/theme/v2/*.css"):
    if f.endswith("z-olcek.css"):
        continue
    s = re.sub(r"/\*.*?\*/", "", open(f, encoding="utf-8").read(), flags=re.S)
    for ortam, sel, gov in ayristir(s):
        # YALNIZ font-size BİLDİREN kural sayılır. Yoksa v2 o seçiciye
        # başka bir şey (renk, kenarlık) yazmış demektir; boyutu yine
        # custom.min.css veriyordur ve override gerekir.
        if not re.search(r"(?:^|;)\s*font-size\s*:", gov):
            continue
        for tek in sel.split(","):
            v2_secici.add((tuple(ortam), re.sub(r"\s+", " ", tek.strip())))

# --- custom.min.css'i tara --------------------------------------------------
src = re.sub(r"/\*.*?\*/", "", open(KAYNAK, encoding="utf-8").read(), flags=re.S)

kurallar, atlanan_ikon, atlanan_v2 = [], 0, 0
for ortam, sel, gov in ayristir(src):
    m = re.search(r"(?:^|;)\s*font-size\s*:\s*([^;}\n]+)", gov)
    if not m:
        continue
    yeni = deger_cevir(m.group(1))
    if not yeni:
        continue
    sel_d = re.sub(r"\s+", " ", sel)
    if IKON.search(sel_d):
        atlanan_ikon += 1
        continue
    # Ortam sorgusu da anahtarın parçası: v2'nin (min-width:768px) içindeki
    # kuralı, custom'ın (max-width:767.98px) kuralını kapatmaz.
    if all((tuple(ortam), re.sub(r"\s+", " ", t.strip())) in v2_secici
           for t in sel_d.split(",")):
        atlanan_v2 += 1
        continue
    kurallar.append((tuple(ortam), sel_d, yeni, m.group(1).strip()))

# --- yaz --------------------------------------------------------------------
gruplar = collections.OrderedDict()
for ortam, sel, yeni, eski in kurallar:
    gruplar.setdefault(ortam, []).append((sel, yeni, eski))

out = ["""/* ============================================================================
   v2 / Z-OLCEK — tipografi merdiveni · custom.min.css override'ları
   ÜRETİLMİŞ DOSYA. ELLE DÜZENLEME.   python3 docs/parts/olcek-uret.py

   Merdiven: 11 · 12,5 · 14 · 16 · 18 · 22 · 26 · 30 · 36
   custom.min.css'teki merdiven dışı her font-size bildirimi, AYNI seçici
   ve AYNI ortam sorgusu içinde en yakın kademeye çekilir. Kaynak dosya
   donmuş: /v1/ arşivi onu paylaşıyor (v1-kopya.py yalnız HTML kopyalar).

   Yükleme sırası v2.css içinde İLK: custom.min.css'i yener, v2'nin kendi
   parçalarını yenmez. v2'de zaten tanımlı seçiciler atlanır.

   Kapsam dışı: ikon/glif seçicileri ve 40px üstü dekoratif ölçüler.
   ========================================================================== */
"""]
for ortam, satirlar in gruplar.items():
    girinti = ""
    if ortam:
        for o in ortam:
            out.append("\n%s%s {\n" % (girinti, o))
            girinti += "  "
    else:
        out.append("\n")
    for sel, yeni, eski in satirlar:
        out.append("%s%s { font-size: %s; }  /* %s */\n" % (girinti, sel, yeni, eski))
    for _ in ortam:
        girinti = girinti[:-2]
        out.append("%s}\n" % girinti)

open(HEDEF, "w", encoding="utf-8").write("".join(out))
print("%d kural -> %s" % (len(kurallar), HEDEF))
print("atlanan — ikon/glif: %d · v2'de zaten tanımlı: %d" % (atlanan_ikon, atlanan_v2))
say = collections.Counter((e, y) for _, _, y, e in kurallar)
for (e, y), c in say.most_common(30):
    print("  %-24s -> %-24s %d" % (e, y, c))
