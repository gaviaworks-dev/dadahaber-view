#!/usr/bin/env bash
# v2'yi yayına alır: v2 -> main birleştirme + /v1/ arşiv kopyası.
# Fikir: v1 dalı ve v1-donmus etiketi hiç değişmez; main'deki /v1/ klasörü
# o daldan HER SEFERİNDE yeniden üretilir, elle düzenlenmez.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

[ -z "$(git status --porcelain)" ] || { echo "HATA: çalışma dizini kirli."; exit 1; }

echo "== v2 -> main"
git checkout main
git merge v2 --no-edit

echo "== /v1/ arşiv kopyası üretiliyor (v1 dalından)"
rm -rf v1
python3 docs/parts/v1-kopya.py v1

echo "== /v1/ kopyası main'e alınıyor"
# .gitignore'daki v1/ kuralı v2 çalışma dalı içindir; main'de kopya izlenir.
git add -f v1
git commit -q -m "v1 arşiv kopyası — /v1/ (v1 dalından üretildi, elle düzenlenmez)" || echo "  (değişiklik yok)"

echo "== push"
git push origin main

echo
echo "Yayın:"
echo "  v2  https://gaviaworks-dev.github.io/dadahaber-view/"
echo "  v1  https://gaviaworks-dev.github.io/dadahaber-view/v1/"
