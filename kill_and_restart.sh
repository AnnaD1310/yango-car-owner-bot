#!/bin/bash

cd /Users/annadolgova/yango-car-owner-bot

echo "=== ПОЛНАЯ ОСТАНОВКА ВСЕХ ПРОЦЕССОВ БОТА ==="

# Убиваем все процессы Python
killall -9 python3 2>/dev/null
killall -9 python 2>/dev/null
pkill -9 -f "main.py" 2>/dev/null
pkill -9 -f "python.*main" 2>/dev/null

# Ждем
sleep 5

# Удаляем lock файл
rm -f .bot.lock

# Проверяем, что все остановлено
PROCESSES=$(ps aux | grep -E "[p]ython.*main|[p]ython3.*main" | wc -l | tr -d ' ')
if [ "$PROCESSES" -gt 0 ]; then
    echo "⚠️  ВНИМАНИЕ: Все еще найдено процессов: $PROCESSES"
    ps aux | grep -E "[p]ython.*main|[p]ython3.*main" | grep -v grep
    echo ""
    echo "Попытка убить еще раз..."
    killall -9 python3 2>/dev/null
    sleep 3
else
    echo "✅ Все процессы остановлены"
fi

# Очистка
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

echo ""
echo "=== ЗАПУСК БОТА ==="
python3 main.py > bot.log 2>&1 &
BOT_PID=$!
echo "Запущен процесс с PID: $BOT_PID"

sleep 10

echo ""
echo "=== ПРОВЕРКА СТАТУСА ==="
if ps -p $BOT_PID > /dev/null 2>&1; then
    echo "✅ Процесс $BOT_PID работает"
else
    echo "❌ Процесс $BOT_PID не найден"
fi

echo ""
echo "=== ПРОВЕРКА ЛОГОВ ==="
tail -20 bot.log 2>/dev/null | strings | grep -E "(started|Error|Conflict|Menu structure)" | head -5 || tail -10 bot.log 2>/dev/null | strings | tail -5

echo ""
echo "=== ГОТОВО ==="
echo "Проверьте логи: tail -f bot.log"

