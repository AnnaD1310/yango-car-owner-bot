#!/usr/bin/env bash
set -e

echo "[обнови бота] git add ."
git add .

echo "[обнови бота] git commit -m 'update'"
git commit -m "update" || echo "[обнови бота] Нет изменений для коммита"

echo "[обнови бота] git push"
git push
