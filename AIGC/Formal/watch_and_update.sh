#!/bin/bash
# 监控 punishments 目录变化，自动更新 index.html
# 使用 fswatch (macOS 自带)

WATCH_DIR="/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/.secret/punishments"
SCRIPT="/Users/gemini/Projects/Own/Antigravity/AntigravityFixed/AIGC/generate_secret_log_v6.py"
PYTHON="/opt/anaconda3/bin/python3"
COOLDOWN=5  # 防抖：5秒内多次变更只执行一次

echo "[Watcher] 开始监控 $WATCH_DIR ..."
echo "[Watcher] 变化检测冷却时间: ${COOLDOWN}s"

LAST_RUN=0

fswatch -r --event Created --event Updated --event Removed "$WATCH_DIR" | while read -r event; do
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_RUN))
    if [ $DIFF -ge $COOLDOWN ]; then
        LAST_RUN=$NOW
        echo "[Watcher $(date +%H:%M:%S)] 检测到变化: $event"
        echo "[Watcher $(date +%H:%M:%S)] 正在重建 index.html ..."
        $PYTHON "$SCRIPT" 2>&1
        echo "[Watcher $(date +%H:%M:%S)] index.html 已更新"
    fi
done
