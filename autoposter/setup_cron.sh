#!/bin/bash
# Устанавливает cron для автопостинга @bahmetev_ai
# Запускать: bash setup_cron.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON=$(which python3)
CRON_JOB="* * * * * $PYTHON $SCRIPT_DIR/scheduler.py >> $SCRIPT_DIR/autoposter.log 2>&1"

# Добавить задание если его ещё нет
(crontab -l 2>/dev/null | grep -v "scheduler.py"; echo "$CRON_JOB") | crontab -

echo "Cron настроен. Скрипт запускается каждую минуту."
echo "Логи: $SCRIPT_DIR/autoposter.log"
echo ""
echo "Расписание публикаций:"
grep '"datetime"' $SCRIPT_DIR/posts.py | sed 's/.*"\(.*\)".*/  \1/'
