#!/usr/bin/env python3
"""
道层 Stage→SOP 路由矩阵验证脚本 v1.0
验证 pipeline-data/stage-to-sop-routing.json 的合规性。

验证项:
  1. JSON 文件加载
  2. 七阶全量覆盖 (stage_id 1-7)
  3. 七阶名称枚举正确 (不会/模糊/清晰/框架/运用/熟练/创新)
  4. primary_flywheels 严格六飞轮枚举
  5. eight_step_focus step_id ∈ {1-8} + step_name 合规
  6. confidence_required ∈ (0, 1]
  7. 路由覆盖递进合理性 (高阶 confidence_required ≥ 低阶)
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ROUTING_PATH = REPO_ROOT / "pipeline-data" / "stage-to-sop-routing.json"

VALID_STAGES = {
    1: "不会", 2: "模糊", 3: "清晰", 4: "框架",
    5: "运用", 6: "熟练", 7: "创新"
}
VALID_FLYWHEELS = {"计划", "预习", "复习", "听课", "作业", "考试"}
VALID_STEP_NAMES = {
    1: "穿透", 2: "提取", 3: "整理", 4: "审题",
    5: "流程", 6: "批改", 7: "分析", 8: "估分"
}
VALID_PRIORITIES = {"必做", "强化", "巩固", "精进"}

PASS_COUNT = 0
FAIL_COUNT = 0
ERRORS: list[str] = []


def ok(msg: str) -> None:
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"  ✅ {msg}")


def fail(msg: str) -> None:
    global FAIL_COUNT
    FAIL_COUNT += 1
    ERRORS.append(f"❌ {msg}")
    print(f"  ❌ {msg}")


def main() -> None:
    print("=" * 60)
    print("  Stage→SOP 路由矩阵验证 v1.0")
    print("=" * 60)

    # [1] 文件加载
    print("\n[1] 文件加载")
    if not ROUTING_PATH.exists():
        fail(f"找不到路由文件: {ROUTING_PATH}")
        sys.exit(1)
    routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
    ok("stage-to-sop-routing.json 加载成功")
    matrix = routing.get("routing_matrix", [])

    # [2] 七阶全量覆盖
    print("\n[2] 七阶全量覆盖 (stage_id 1-7)")
    found_stages = {r["stage_id"] for r in matrix}
    missing_stages = set(VALID_STAGES.keys()) - found_stages
    extra_stages = found_stages - set(VALID_STAGES.keys())
    if missing_stages:
        fail(f"缺少阶位: {missing_stages}")
    else:
        ok("七阶 1-7 全量覆盖 ✓")
    if extra_stages:
        fail(f"含非法 stage_id: {extra_stages}")
    else:
        ok("无多余 stage_id ✓")

    # [3] 七阶名称枚举
    print("\n[3] 七阶名称枚举")
    for r in matrix:
        sid = r.get("stage_id")
        sname = r.get("stage_name", "")
        expected = VALID_STAGES.get(sid, "?")
        if sname == expected:
            ok(f"stage {sid} name='{sname}' ✓")
        else:
            fail(f"stage {sid} name='{sname}' 期望 '{expected}'")

    # [4] primary_flywheels 枚举
    print("\n[4] primary_flywheels 严格六飞轮枚举")
    for r in matrix:
        sid = r.get("stage_id")
        fws = r.get("primary_flywheels", [])
        if not fws:
            fail(f"stage {sid}: primary_flywheels 为空")
        for fw in fws:
            if fw not in VALID_FLYWHEELS:
                fail(f"stage {sid}: 飞轮 '{fw}' 不在六飞轮枚举 {VALID_FLYWHEELS}")
            else:
                ok(f"stage {sid}: 飞轮 '{fw}' 合规 ✓")

    # [5] eight_step_focus 合规
    print("\n[5] eight_step_focus step_id + step_name 合规")
    for r in matrix:
        sid = r.get("stage_id")
        steps = r.get("eight_step_focus", [])
        for s in steps:
            step_id = s.get("step_id")
            step_name = s.get("step_name", "")
            priority = s.get("priority", "")
            expected_name = VALID_STEP_NAMES.get(step_id, "?")
            if step_id not in VALID_STEP_NAMES:
                fail(f"stage {sid}: step_id={step_id} 不在 {{1-8}}")
            elif step_name != expected_name:
                fail(f"stage {sid}: step {step_id} name='{step_name}' 期望 '{expected_name}'")
            else:
                ok(f"stage {sid}: 步 {step_id}'{step_name}' ✓")
            if priority not in VALID_PRIORITIES:
                fail(f"stage {sid}: step {step_id} priority='{priority}' 不合规")

    # [6] confidence_required 范围
    print("\n[6] confidence_required ∈ (0, 1]")
    for r in matrix:
        sid = r.get("stage_id")
        cr = r.get("confidence_required")
        if cr is None or not (0 < cr <= 1.0):
            fail(f"stage {sid}: confidence_required={cr} 超出 (0,1]")
        else:
            ok(f"stage {sid}: confidence_required={cr} ✓")

    # [7] 递进合理性 (高阶 confidence ≥ 低阶)
    print("\n[7] confidence_required 递进合理性")
    sorted_stages = sorted(matrix, key=lambda r: r["stage_id"])
    for i in range(1, len(sorted_stages)):
        prev = sorted_stages[i - 1]
        curr = sorted_stages[i]
        if curr["confidence_required"] < prev["confidence_required"]:
            fail(f"stage {curr['stage_id']} confidence={curr['confidence_required']} < "
                 f"stage {prev['stage_id']} confidence={prev['confidence_required']} (递进方向错误)")
        else:
            ok(f"stage {prev['stage_id']}→{curr['stage_id']}: "
               f"{prev['confidence_required']}→{curr['confidence_required']} 递进合规 ✓")

    # ── 结果 ──────────────────────────────────────────────────────
    print(f"\n{'=' * 60}")
    total = PASS_COUNT + FAIL_COUNT
    print(f"  结果: {PASS_COUNT}/{total} 通过 | {FAIL_COUNT} 失败")
    print("=" * 60)
    if FAIL_COUNT > 0:
        print("\n失败详情:")
        for e in ERRORS:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("  ✅ Stage→SOP 路由矩阵验证 PASS — 七阶路由全部合规")
        sys.exit(0)


if __name__ == "__main__":
    main()
