#!/bin/bash
cd /Users/annadolgova/yango-car-owner-bot
echo "🛑 Останавливаю старые процессы..."
pkill -9 -f "python.*main.py" 2>/dev/null
sleep 2
echo "🧹 Очищаю кеш..."
rm -f .bot.lock
rm -rf __pycache__
echo "🚀 Запускаю бота с новым кодом..."
python3 main.py > bot.log 2>&1 &
sleep 5
if ps aux | grep -q "[p]ython3 main.py"; then
    echo "✅ Бот запущен!"
    echo ""
    echo "📋 Последние строки лога:"
    tail -5 bot.log 2>/dev/null || echo "(лог пуст)"
else
    echo "❌ Бот не запустился. Проверьте bot.log"
    tail -20 bot.log 2>/dev/null
fi
