#!/bin/bash

cd /Users/annadolgova/yango-car-owner-bot

echo "=== ПОЛНАЯ ОСТАНОВКА ВСЕХ ПРОЦЕССОВ ==="
pkill -9 -f "python.*main.py" 2>/dev/null
pkill -9 -f "python3.*main.py" 2>/dev/null
sleep 3

# Проверка, что все остановлено
PROCESSES=$(ps aux | grep "[p]ython.*main.py" | wc -l | tr -d ' ')
if [ "$PROCESSES" -gt 0 ]; then
    echo "⚠️  ВНИМАНИЕ: Все еще запущено процессов: $PROCESSES"
    ps aux | grep "[p]ython.*main.py"
    echo "Попытка остановить еще раз..."
    pkill -9 -f "python.*main.py" 2>/dev/null
    sleep 2
else
    echo "✅ Все процессы остановлены"
fi

echo ""
echo "=== ОЧИСТКА ==="
rm -f .bot.lock
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
echo "✅ Очищено"

echo ""
echo "=== ЗАПУСК БОТА (ОДИН ЭКЗЕМПЛЯР) ==="
python3 main.py > bot.log 2>&1 &
BOT_PID=$!
echo "PID: $BOT_PID"

sleep 8

echo ""
echo "=== ПРОВЕРКА ЛОГОВ ==="
if [ -f bot.log ]; then
    echo "Последние 50 строк лога:"
    tail -50 bot.log | grep -E "(DEBUG.*build_main_menu|DEBUG.*Root node|Menu structure validation|start_polling|Error|ERROR|Conflict|what_is_coa|Bot.*started)" | head -20 || echo "--- Полный лог (последние 30 строк):" && tail -30 bot.log
else
    echo "❌ Файл bot.log не найден"
fi

echo ""
echo "=== ПРОВЕРКА ПРОЦЕССОВ ==="
PROCESSES=$(ps aux | grep "[p]ython.*main.py" | wc -l | tr -d ' ')
if [ "$PROCESSES" -eq 1 ]; then
    echo "✅ Запущен ровно один процесс бота"
    ps aux | grep "[p]ython.*main.py" | grep -v grep
else
    echo "⚠️  Запущено процессов: $PROCESSES (ожидается 1)"
    ps aux | grep "[p]ython.*main.py" | grep -v grep
fi

echo ""
echo "=== ИНСТРУКЦИИ ==="
echo "1. Откройте Telegram и отправьте /start"
echo "2. Проверьте, что кнопка 'How it works' есть первой в списке"
echo "3. Перейдите в любой раздел и вернитесь назад (или нажмите Home)"
echo "4. Кнопка 'How it works' должна оставаться первой"
echo ""
echo "Для просмотра логов в реальном времени: tail -f bot.log"
echo "Для остановки бота: pkill -9 -f 'python.*main.py'"

