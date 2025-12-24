#!/bin/bash

echo "=========================================="
echo "ПОЛНАЯ ПЕРЕЗАГРУЗКА БОТА"
echo "=========================================="
echo ""

# Шаг 1: Остановка ВСЕХ процессов Python
echo "1. Остановка всех процессов Python..."
killall -9 python3 2>/dev/null
killall -9 python 2>/dev/null
pkill -9 -f "main.py" 2>/dev/null
pkill -9 python 2>/dev/null
sleep 3

# Шаг 2: Проверка что все остановлено
echo ""
echo "2. Проверка процессов..."
PROCESSES=$(ps aux | grep -E "[p]ython.*main|[p]ython3.*main" | wc -l | tr -d ' ')
if [ "$PROCESSES" -gt 0 ]; then
    echo "   ⚠️  Найдено процессов: $PROCESSES"
    ps aux | grep -E "[p]ython.*main|[p]ython3.*main" | grep -v grep
    echo ""
    echo "   Попытка более агрессивной остановки..."
    ps aux | grep -E "[p]ython.*main|[p]ython3.*main" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
    sleep 3
else
    echo "   ✅ Все процессы остановлены"
fi

# Шаг 3: Удаление lock файла
echo ""
echo "3. Удаление lock файла..."
rm -f .bot.lock
echo "   ✅ Lock файл удален"

# Шаг 4: Очистка кэша Python
echo ""
echo "4. Очистка кэша Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
echo "   ✅ Кэш очищен"

# Шаг 5: Запуск бота
echo ""
echo "5. Запуск бота..."
cd "$(dirname "$0")"
python3 main.py > bot.log 2>&1 &
BOT_PID=$!
echo "   ✅ Бот запущен с PID: $BOT_PID"

# Шаг 6: Ожидание и проверка
echo ""
echo "6. Ожидание запуска (15 секунд)..."
sleep 15

# Шаг 7: Проверка статуса
echo ""
echo "7. Проверка статуса..."
if ps -p $BOT_PID > /dev/null 2>&1; then
    echo "   ✅ Процесс $BOT_PID работает"
else
    echo "   ❌ Процесс не найден!"
fi

# Шаг 8: Проверка логов на ошибки
echo ""
echo "8. Проверка логов (последние 20 строк)..."
if [ -f bot.log ]; then
    tail -20 bot.log | strings | tail -15
else
    echo "   ⚠️  Лог файл не найден"
fi

echo ""
echo "=========================================="
echo "ГОТОВО!"
echo "=========================================="
echo ""
echo "Проверьте бота в Telegram:"
echo "1. Отправьте /start"
echo "2. Проверьте что кнопка 'How it works' есть и она первая"
echo "3. Перейдите в любой раздел и вернитесь назад"
echo "4. Кнопка 'How it works' должна оставаться на месте"
echo ""

