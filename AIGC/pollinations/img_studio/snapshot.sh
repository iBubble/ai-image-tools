#!/bin/bash
# ============================================================
#  Image Studio 快照备份与回滚工具
#  用法:
#    ./snapshot.sh save  [备注]    — 创建快照
#    ./snapshot.sh list            — 列出所有快照
#    ./snapshot.sh rollback <名称> — 回滚到指定快照
#    ./snapshot.sh diff <名称>     — 查看差异
#    ./snapshot.sh delete <名称>   — 删除快照
# ============================================================
set -e
cd "$(dirname "$0")"

ACTION="${1:-list}"
NOTE="${2:-}"

case "$ACTION" in
save)
    git add -A
    git diff --cached --quiet 2>/dev/null || \
        git commit -m "snapshot: 快照前自动保存"
    TAG="snapshot_$(date +%Y%m%d_%H%M%S)"
    MSG="${NOTE:-$(date +%Y-%m-%d_%H:%M:%S)}"
    git tag -a "$TAG" -m "📸 $MSG"
    echo "✅ 快照: $TAG ($MSG)"
    echo "   回滚: ./snapshot.sh rollback $TAG"
    ;;
list)
    echo "📋 所有快照:"
    echo "──────────────────────────────────"
    git tag -l "snapshot_*" --sort=-creatordate | while read t; do
        M=$(git tag -l "$t" -n1 | sed "s/^$t *//")
        H=$(git rev-list -1 "$t" | cut -c1-8)
        echo "  $t [$H] $M"
    done
    C=$(git tag -l "snapshot_*" | wc -l | tr -d ' ')
    echo "────────────────── 共 ${C} 个快照"
    ;;
rollback)
    [ -z "$NOTE" ] && echo "❌ 用法: ./snapshot.sh rollback snapshot_xxx" && exit 1
    SAFE="snapshot_safety_$(date +%Y%m%d_%H%M%S)"
    git add -A
    git diff --cached --quiet 2>/dev/null || \
        git commit -m "snapshot: 回滚前安全快照"
    git tag -a "$SAFE" -m "🛡️ 回滚前自动安全快照"
    echo "🛡️ 安全快照: $SAFE"
    git reset --hard "$NOTE"
    echo "✅ 已回滚到: $NOTE"
    echo "   撤销: ./snapshot.sh rollback $SAFE"
    ;;
diff)
    [ -z "$NOTE" ] && echo "❌ 请指定快照名称" && exit 1
    git diff "$NOTE" --stat
    ;;
delete)
    [ -z "$NOTE" ] && echo "❌ 请指定快照名称" && exit 1
    git tag -d "$NOTE"
    echo "🗑️ 已删除: $NOTE"
    ;;
*)
    echo "用法: ./snapshot.sh {save|list|rollback|diff|delete} [参数]"
    ;;
esac
