#!/usr/bin/env bash
# 道层零漂移守护脚本 v5.1
# 道层 Compliance: v5.1 | grep 6 漂移=0 命中
# 用法: bash scripts/.dao-guard.sh [目录]
set -euo pipefail

SCAN_ROOT="${1:-.}"
FAIL=0

echo "=== 道层零漂移守护 v5.1 ==="
echo "扫描目录: $SCAN_ROOT"
echo ""

scan_pattern() {
  local pattern="$1"
  local label="$2"
  local dirs=()
  for d in pipeline-data schemas coaching-sops docs services apps; do
    [ -d "$SCAN_ROOT/$d" ] && dirs+=("$SCAN_ROOT/$d")
  done
  if [ ${#dirs[@]} -eq 0 ]; then
    echo "✅ [$label] 无可扫描目录，跳过"
    return
  fi
  local hits
  hits=$(grep -rEl --include="*.json" --include="*.md" --include="*.ts" --include="*.py" \
    "$pattern" "${dirs[@]}" 2>/dev/null | wc -l | tr -d ' ') || true
  if [ "$hits" -gt 0 ]; then
    echo "❌ [$label] 漂移命中 $hits 文件:"
    grep -rEl --include="*.json" --include="*.md" --include="*.ts" --include="*.py" \
      "$pattern" "${dirs[@]}" 2>/dev/null | head -5
    FAIL=1
  else
    echo "✅ [$label] 0 命中"
  fi
}

# 检查 1: MECE 绝不是 Mutually Exclusive
scan_pattern "Mutually Exclusive" "MECE-漂移"

# 检查 2: 八步⑤=流程，绝不含"演示"
scan_pattern "演示" "八步⑤-漂移"

# 检查 3: 六飞轮 — 无错题/笔记/阅读/实践飞轮
scan_pattern "错题飞轮|笔记飞轮|阅读飞轮|实践飞轮" "六飞轮-漂移"

# 检查 4: JUMEQ 不含明文全称
scan_pattern "Judge.*Understand|Understand.*Match" "JUMEQ-漂移"

# 检查 5: CAMIQ 不含明文全称
scan_pattern "Categorize.*Integrate|Integrate.*Query" "CAMIQ-漂移"

# 检查 6: 七阶 不含替代词
scan_pattern "导入阶段|拆解阶段|讲解法|类比法" "七阶-漂移"

echo ""
if [ "$FAIL" -eq 1 ]; then
  echo "❌ 道层守护 FAIL — 请修正漂移后重新运行"
  exit 1
else
  echo "✅ 道层守护 PASS — 6/6 0 命中"
  exit 0
fi
