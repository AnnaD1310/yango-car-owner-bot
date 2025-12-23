#!/bin/bash

cd /Users/annadolgova/yango-car-owner-bot

echo "🛑 Останавливаю все процессы бота..."
pkill -9 -f "python.*main.py" 2>/dev/null
sleep 2

echo "🧹 Очищаю кеш и lock файлы..."
rm -f .bot.lock
rm -rf __pycache__
find . -name "*.pyc" -delete 2>/dev/null

echo ""
echo "✅ Проверка FAQ в коде:"
if grep -q "What is the Car Owner Acquisition program" main.py && \
   grep -q "@AnnaD1" main.py && \
   grep -q "@nikharpatel09" main.py; then
    echo "   ✅ FAQ обновлен правильно!"
else
    echo "   ❌ FAQ не найден в коде!"
    exit 1
fi

echo ""
echo "🚀 Запускаю бота..."
python3 main.py > bot.log 2>&1 &
BOT_PID=$!

sleep 5

if ps -p $BOT_PID > /dev/null 2>&1; then
    echo "✅ Бот запущен (PID: $BOT_PID)"
    echo ""
    echo "📋 Последние строки лога:"
    tail -10 bot.log 2>/dev/null || echo "(лог пуст)"
    echo ""
    echo "📱 В Telegram:"
    echo "   1. Отправьте /start заново"
    echo "   2. Откройте раздел: ❓ FAQ"
    echo "   3. Вы должны увидеть 8 новых вопросов"
else
    echo "❌ Бот не запустился!"
    echo ""
    echo "📋 Ошибки из лога:"
    tail -30 bot.log 2>/dev/null
    exit 1
fi


