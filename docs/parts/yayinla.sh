#!/usr/bin/env bash
# v2'yi yayına alır.
#
# main bir ÇALIŞMA DALI DEĞİL, ÜRETİLMİŞ YAYIN AĞACIDIR. Her yayında
# v2 dalının içeriğinden yeniden kurulur; elle düzenlenmez.
#
# Yayındaki yapı:
#   /          yönlendirme -> /v2/
#   /v2/       sitenin kendisi (tek gerçek kopya)
#   /v1/       donmuş arşiv, v1 dalından üretilir
#   /assets/   ortak varlık ağacı, sürümler ../assets/ ile paylaşır
#   /404.html  Pages yalnız KÖK 404'ünü kullanır
#
# Neden merge değil: main'de kök HTML'ler /v2/ altına taşındığı için
# `git merge v2` her seferinde modify/delete çakışması üretirdi.
# Bunun yerine v2'nin içeriği main'e "checkout" edilip ağaç yeniden kurulur.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

SURUM="${1:-v2}"
DAL="$SURUM"

[ -z "$(git status --porcelain)" ] || { echo "HATA: çalışma dizini kirli."; exit 1; }

echo "== statik denetim ($DAL dalı)"
git checkout -q "$DAL"
python3 docs/parts/denetim.py

echo "== v2.css düzleştiriliyor (yayında @import zinciri istenmiyor)"
python3 docs/parts/duzlestir.py
if ! git diff --quiet assets/css/theme/v2.css; then
  git add assets/css/theme/v2.css
  git commit -q -m "v2.css düzleştirildi (yayın)"
  git push -q origin "$DAL"
fi

echo "== main yayın ağacı kuruluyor"
git checkout -q main
# önceki üretimi temizle: kök sayfalar, sürüm klasörleri
git rm -q -r --ignore-unmatch --cached "$SURUM" v1 >/dev/null 2>&1 || true
rm -rf "$SURUM" v1
git ls-files -z '*.html' | xargs -0 -r git rm -q -f >/dev/null 2>&1 || true
# çalışma dalının içeriğini al
git checkout "$DAL" -- .

echo "== kök sayfalar /$SURUM/ altına taşınıyor + köke yönlendirme"
python3 docs/parts/surum-kur.py "$SURUM"

echo "== /v1/ arşiv kopyası üretiliyor (v1 dalından)"
python3 docs/parts/v1-kopya.py v1

# .gitignore'daki v1/ ve v2/ kuralları ÇALIŞMA dalı içindir; main'de kopyalar izlenir.
git add -f "$SURUM" v1 >/dev/null
git add -A >/dev/null

echo "== yayın ağacı doğrulanıyor"
python3 - "$SURUM" <<'PY'
import os, sys
s = sys.argv[1]
hata = []
if not os.path.exists("index.html"): hata.append("kökte index.html yok")
elif "url=./%s/" % s not in open("index.html", encoding="utf-8").read():
    hata.append("kök index.html %s'ye yönlendirmiyor" % s)
if not os.path.exists("404.html"): hata.append("kökte 404.html yok (Pages yalnız kök 404'ünü kullanır)")
for d, n in ((s, 80), ("v1", 60)):
    a = len([x for x in os.listdir(d) if x.endswith(".html")]) if os.path.isdir(d) else 0
    if a < n: hata.append("%s/ altında yalnız %d sayfa (beklenen >=%d)" % (d, a, n))
if not os.path.isdir("assets/css/theme"): hata.append("assets/ kökte yok")
kok_html = [x for x in os.listdir(".") if x.endswith(".html")]
if sorted(kok_html) != ["404.html", "index.html"]:
    hata.append("kökte beklenmeyen sayfa: %s" % ", ".join(sorted(set(kok_html) - {"404.html", "index.html"})[:5]))
if hata:
    print("HATA:"); [print("  ✗", h) for h in hata]; sys.exit(1)
print("  yayın ağacı doğru")
PY

git commit -q -m "Yayın — /$SURUM/ site · / yönlendirme · /v1/ arşiv (üretildi, elle düzenlenmez)" \
  || echo "  (değişiklik yok)"

echo "== push"
git push origin main
git checkout -q "$DAL"

echo
echo "Yayın:"
echo "  v2  https://gaviaworks-dev.github.io/dadahaber-view/$SURUM/"
echo "  v1  https://gaviaworks-dev.github.io/dadahaber-view/v1/"
echo "  kök https://gaviaworks-dev.github.io/dadahaber-view/  -> /$SURUM/ yönlendirir"
